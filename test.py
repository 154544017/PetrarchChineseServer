tb_str= """CREATE TABLE `rs_analysis_event_library` (
`id` int(11) NOT NULL,
`name` varchar(255) NOT NULL,
`file_name` varchar(255) NOT NULL,
`create_user` int(11) NOT NULL,
`create_time` datetime NOT NULL,
PRIMARY KEY (`id`),
KEY `rf_user_idx` (`create_user`),
CONSTRAINT `rf_eve_user` FOREIGN KEY (`create_user`) REFERENCES `rs_user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;"""
print(tb_str)