using System;
using System.ComponentModel.DataAnnotations;

namespace YoonDongju.Data
{
    public class Notice
    {
        public Notice (string title, string content)
        {
            Title = title;
            Content = content;
        }
        [Required(ErrorMessage = "제목이 있어야 합니다.")]
        [StringLength(64, ErrorMessage = "제목은 64자 이하여야 합니다.")]
        public string Title { get; set; }
        [Required(ErrorMessage = "본문이 있어야 합니다.")]
        public string Content { get; set; }
        // [Required]
        // public string Author { get; set; }
        // [Required]
        // public DateTime published { get; set; }
    }
}