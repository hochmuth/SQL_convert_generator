Get-ChildItem *.csv | % { Get-Content $_ | Out-File -Encoding BigEndianUnicode "$($_.basename)-BE.csv" }
