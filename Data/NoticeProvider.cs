using System;
using System.Threading.Tasks;
using Microsoft.Data.Sqlite;

namespace YoonDongju.Data
{
    public class NoticeProvider
    {
        public static Task<object> GetNoticeList(int skip, int count)
        {
            using (var DB = new SqliteConnection("Data Source=test.db"))
            {
                DB.OpenAsync();
                var command = DB.CreateCommand();
                command.CommandText =
                @$"
                    SELECT title
                    FROM notices
                    LIMIT {skip} {count};
                ";
                object result = command.ExecuteScalarAsync();
                return Task.FromResult(result);
            }
        }
    }
}