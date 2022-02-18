for db in $(ls sql)
do
    cp "sql/$db" "/home/ubuntu/backup/$db.backup.$(date +'%Y-%m-%d').db"
done