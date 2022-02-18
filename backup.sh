for db in $(ls sql)
do
    cp -R "sql/$db" "~/backup/$db.backup.$(date +'%Y-%m-%d').db"
done