using System;
using Microsoft.Data.Sqlite;

namespace YoonDongju.Data
{
    public class NoticeProvider
    {
        public static void GetNoticeList(int from, int offset)
        {
            using (var DB = new SqliteConnection("Data Source=test.db"))
            {
                DB.Open();
                var command = DB.CreateCommand();
                command.CommandText =
                @$"
                    SELECT title
                    FROM notices
                    LIMIT {from} OFFSET {offset};
                ";
                using (var reader = command.ExecuteReader())
                {
                    while (reader.Read())
                    {
                        var row = reader.GetString(0);
                        Console.WriteLine(row);
                    }
                }
            }
        }
    }
}