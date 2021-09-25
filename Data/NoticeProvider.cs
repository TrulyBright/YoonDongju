using Microsoft.Data.Sqlite;
using System.Collections.Generic;

namespace YoonDongju.Data
{
    public class NoticeProvider
    {
        public static List<Notice> GetNoticeList(int skip, int count)
        {
            using (var DB = new SqliteConnection("Data Source=test.db"))
            {
                DB.Open();
                var command = DB.CreateCommand();
                command.CommandText =
                @$"
                    SELECT title
                    FROM notices
                    LIMIT {skip}, {count};
                ";
                using (var reader = command.ExecuteReader())
                {
                    List<Notice> list = new List<Notice>();
                    while (reader.Read())
                    {
                        list.Add(new Notice(reader.GetString(0), reader.GetString(1)));
                    }
                    return list;
                }
            }
        }
    }
}