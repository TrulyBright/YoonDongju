using System;
using Microsoft.Data.Sqlite;

namespace YoonDongju.Data
{
    public class NoticeProvider
    {
        public static object GetNoticeList(int skip, int count)
        {
            using (var DB = new SqliteConnection("Data Source=test.db"))
            {
                DB.Open();
                var command = DB.CreateCommand();
                command.CommandText =
                @$"
                    SELECT title
                    FROM notices
                    LIMIT {skip} {count};
                ";
                object result = command.ExecuteScalar();
                return result;
            }
        }
    }
}