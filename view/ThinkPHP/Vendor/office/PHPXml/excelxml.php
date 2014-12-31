<?php

/**
 * Class ExcelXML
 * Provide functions to modify the content of file in Excel's XML format.
 * 
 * REQUIRED:
 * - An ExcelXML file as template
 * 
 * FEATURES:
 * - read, modify, and save Excel's XML file
 * - create download stream as Excel file format (*.xls)
 * 
 * CHANGELOG:
 * 06-08-2008
 * - Update setCellValue function
 * - Fix setCellValue bug
 * 13-07-2008
 * - First created 
 * 
 * 
 * @author Herry Ramli (herry13@gmail.com)
 * @license GPL
 * @version 0.1.1
 * @copyright August 06, 2008
 */
class ExcelXML
{
	var $domXML;
	var $activeWorksheet;
	
	function ExcelXML()
	{
	}
	
	/**
	 * Read ExcelXML from file
	 *
	 * @param String $filename
	 * @return boolean true if succeed or false if failed
	 */
	function read($filename)
	{
		$this->domXML = new DOMDocument();
		if (!$this->domXML->load($filename))
			return false;
		$this->activeWorksheet = null;
		return true;
	}
	
	/**
	 * Save ExcelXML to a file
	 *
	 * @param String $filename
	 * @return boolean true if succeed or false if failed
	 */
	function save($filename, $download=false, $download_filename="")
	{
		if (!$download)
		{
			return $this->domXML->save($filename);
		}
		elseif ($this->domXML->save($filename))
		{
			$FileInfo = pathinfo(filename);
			// fix for IE catching or PHP bug issue 
			header("Pragma: public"); 
			header("Expires: 0"); // set expiration time 
			header("Cache-Control: must-revalidate, post-check=0, pre-check=0");  
			// browser must download file from server instead of cache 
			// force download dialog 
			header("Content-Type: application/force-download"); 
			header("Content-Type: application/octet-stream"); 
			header("Content-type: application/x-msexcel");
			header("Content-Type: application/download"); 
			// use the Content-Disposition header to supply a recommended filename and  
			// force the browser to display the save dialog.
			if ($download_filename == "")
				$download_filename = "download.xls";
			header("Content-Disposition: attachment; filename=".$download_filename.";"); 
			header("Content-Transfer-Encoding: binary"); 
			header("Content-Length: ".filesize($filename)); 
			@readfile($filename);
			return true;
		}
		return false;
	}

	/**
	 * Create new table node
	 *
	 * @param Integer $totalRow
	 * @param Integer $totalCol
	 * @return DOMElement
	 */
	function createTableNode($totalRow=0, $totalCol=0)
	{
		// e.g.: <Table ss:ExpandedColumnCount="1" ss:ExpandedRowCount="1" x:FullColumns="1" x:FullRows="1">
		$tableNode = $this->domXML->createElement("Table");
		$tableNode = $this->activeWorksheet->appendChild($tableNode);
		$this->setTableNodeAttributes($tableNode, $totalRow, $totalCol);
		
		return $tableNode;
	}
	
	/**
	 * Set TableNode's attributes
	 *
	 * @param DOMElement $tableNode
	 * @param Integer $row total row
	 * @param Integer $col total column
	 * @return Boolean true if succeed or false if not
	 */
	function setTableNodeAttributes(&$tableNode, $row, $col)
	{
		try {
			$tableNode->setAttribute("ss:ExpandedColumnCount", $col);
			$tableNode->setAttribute("ss:ExpandedRowCount", $row);
			$tableNode->setAttribute("x:FullColumns", 1);
			$tableNode->setAttribute("x:FullRows", 1);
			return true;
		} catch (Exception $e) {
			return false;			
		}
	}
	
	/**
	 * Create DataNode and set the value
	 *
	 * @param Mixed $value
	 * @return DOMElement new DataNode
	 */
	function createDataNode($value="")
	{
		$dataNode = $this->domXML->createElement("Data");
		$dataNode->nodeValue = $value;
		try {
			if (is_numeric($value))
				$dataNode->setAttribute("ss:Type", "Number");
			else
				$dataNode->setAttribute("ss:Type", "String");
		} catch (Exception $e) {
		}
		return $dataNode;
	}
	
	/**
	 * Search and return DOMNode associate with given excel address
	 * 
	 * @param String $address excel address
	 * @return DOMNode or null if not found
	 */
	function getDOMNode($address, $is_create=false)
	{
		$col = $this->getColumnAddress($address);
		$row = $this->getRowAddress($address);
		
		return $this->getDOMNodeByRowColumn($row, $col, $is_create);
	}
	
	/**
	 * Search and return DOMNode associate with given excel address
	 * 
	 * @param Integer $row
	 * @param Integer $col
	 * @return DOMNode or null if not found
	 */
	function getDOMNodeByRowColumn($row, $col, $is_create=false)
	{
		if ($this->activeWorksheet == null)
			return null;
		
		$resetTableAttributes = false;
		
		$tables = $this->activeWorksheet->getElementsByTagName("Table");
		if ($tables->length > 0)
			$tableNode = $tables->item(0);
		elseif ($is_create)
			$tableNode = $this->createTableNode($row, $col);
		else
			return null;

		$rowNodes = $tableNode->getElementsByTagName("Row");
		
		if ($rowNodes->length >= $row)
		{
			$rowNode = $rowNodes->item($row-1);
		}
		elseif ($is_create)
		{
			// create additional row nodes, total new node == $row - $rowNodes->length;
			$totalNewRowNode = $row - $rowNodes->length;
			for ($i=0; $i<$totalNewRowNode; $i++)
				$rowNode = $tableNode->appendChild(new DOMElement("Row"));
			$resetTableAttributes = true;
		}
		else
		{
			return null;
		}
		$colNodes = $rowNode->getElementsByTagName("Cell");
		//echo $row . " - " . $col;
		if ($colNodes->length >= $col)
		{
			$colNode = $colNodes->item($col-1);
		}
		elseif ($is_create)
		{
			// create additional col nodes, total new node == $col - $colNodes->length;
			$totalNewColNode = $col - $colNodes->length;
			for ($i=0; $i<$totalNewColNode; $i++)
				$colNode = $rowNode->appendChild(new DOMElement("Cell"));
			$resetTableAttributes = true;
		}
		else
		{
			return null;
		}
		$this->setTableNodeAttributes($tableNode, $row, $col);
		$dataNodes = $colNode->getElementsByTagName("Data");
		
		if ($dataNodes->length > 0)
		{
			return $dataNodes->item(0);
		}
		elseif ($is_create)
		{
			return $colNode->appendChild($this->createDataNode(""));
		}
		else
		{
			return null;
		}
		
		return null;
	}
	
	/**
	 * Set cell's value with given address
	 *
	 * @param String $address cell's address
	 * @param String $value cell's value
	 * @return boolean true if succeed or false if failed
	 */
	function setCellValue($address, $value)
	{
		$node = $this->getDOMNode($address, true);
		if ($node == null)
			return false;
		$node->nodeValue = $value;
		return true;		
	}
	
	/**
	 * Set cell's value with given address
	 *
	 * @param Integer $row
	 * @param Integer $column
	 * @return boolean true if succeed or false if failed
	 */
	function setCellValueByRowColumn($row, $col, $value)
	{
		$node = $this->getDOMNodeByRowColumn($row, $col, true);
		if ($node == null)
			return false;
		$node->nodeValue = $value;
		return true;
	}

	/**
	 * Get row number of given excel address
	 *
	 * @param String $address excel address
	 * @return int row number
	 */
	function getRowAddress($address)
	{
		$len = strlen($address);
		$index = 0;
		for (; $index<$len; $index++)
		{
			$chr = substr($address, $index, 1);
			if (is_numeric($chr))
				break;
		}
		$addr = substr($address, $index);
		return intval($addr);
	}
	
	/**
	 * Get column number of given excel address
	 *
	 * @param String $address excel address
	 * @return int column number
	 */
	function getColumnAddress($address)
	{
		$addr = strtoupper($address);
		$len = strlen($addr);
		$index = 0;
		for (; $index<$len; $index++)
		{
			$chr = substr($addr, $index, 1);
			if (is_numeric($chr))
				break;
		}
		$colAddr = substr($addr, 0, $index);
		$col = 0;
		for ($i=0; $i<strlen($colAddr); $i++)
		{
			$c = substr($colAddr, -($i+1), 1);
			$d = ord($c) - 64;
			$v = ($i <= 0) ? $d : ($d*26);
			$col += $v;
		}
		return $col; //ord($col) - 64;
	}
	
	/**
	 * Set active worksheet of given index
	 *
	 * @param int $index
	 * @return boolena true if succeed or false if failed
	 */
	function setActiveWorksheetByIndex($index)
	{
		$workbook = $this->domXML->getElementsByTagName("Workbook");
		$workbook = $workbook->item(0);
		$worksheets = $workbook->getElementsByTagName("Worksheet");
		if ($worksheets->length <= 0)
			return false;
		$this->activeWorksheet = $worksheets->item(0);
		return true;
	}
	
	/**
	 * Set active worksheet with given worksheet's name
	 *
	 * @param String $name
	 * @return boolean true if succeed or false if failed
	 */
	function setActiveWorksheet($name)
	{
		$workbook = $this->domXML->getElementsByTagName("Workbook");
		$workbook = $workbook->item(0);
		$worksheets = $workbook->getElementsByTagName("Worksheet");
		if ($worksheets->length <= 0)
			return false;
			
		foreach ($worksheets as $worksheet)
		{
			if ($worksheet->getAttribute("ss:Name") == $name)
			{
				$this->activeWorksheet = $worksheet;
				return true;
			}
		}
		return false;
	}
	
	/**
	 * Return cell's value of given excel address
	 *
	 * @param String $address excel address
	 * @return String
	 */
	function getCellValue($address)
	{
		$node = $this->getDOMNode($address);
		if ($node != null)
			return $node->nodeValue;
		return null; 
	}

	/**
	 * Return cell's value of given excel address
	 *
	 * @param Integer $row
	 * @param Integer $col
	 * @return String
	 */
	function getCellValueByRowColumn($row, $col)
	{
		$node = $this->getDOMNodeByRowColumn($row, $col);
		if ($node != null)
			return $node->nodeValue;
		return null; 
	}
}

?>