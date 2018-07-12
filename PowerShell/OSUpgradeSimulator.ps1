$MachineListFile = "F:\machielist.txt"
$DMClientPath = "D:\app\APTools.ap_07_09_10_8_5005_3683\"
$ProcessingNumber = 0

Push-Location -Path $DMClientPath
if ([System.IO.File]::Exists($MachineListFile)) {
    $FileContent = (Get-Content -Path $MachineListFile)
    foreach($line in $FileContent)
    {
        if((([string]$line).Length -gt 0))
        {
            $ProcessingNumber += 1
            $items =  $line -split ","
            #$Command = $DMClientPath + "dmclient.exe -f -c ""SetMachineStatus -t F -m -s " + $items[0] + """"
            $Command = $DMClientPath + "ManualRepair.exe -a HardReboot -r""Simulate OSUpgrade"" -m " + $items[0]
            echo "Command:" $Command
            $Result = iex $Command
            echo "Result:" $Result

            if ($ProcessingNumber -ge 10)
            {
                Start-Sleep -s 3600
                $ProcessingNumber = 0   
            }
        }
    }
} else {
    echo ($MachineListFile + " doesn't exist")
}
Pop-Location