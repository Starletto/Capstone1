CREATE DATABASE purwadhika;

show databases;

use purwadhika;

show tables;
create table capstone1 (
	id int not null auto_increment primary key,
    nama varchar(50) not null,
    kategori varchar(50),
    harga float,
    stok int,
    terjual int,
    stok_sisa int
);

show tables;
select * from capstone1;

insert into capstone1
values
('2', 'Kopi Susu Gula Aren', 'minuman', 18000, 15),
('3', 'Kaos Polos Cotton', 'pakaian', 75000, 25),
('4', 'Roti Bakar Cokelat', 'makanan', 20000, 12),
('5', 'Teh Tarik Jelly', 'minuman', 15000, 30),
('6', 'Topi Baseball', 'pakaian', 55000, 12),
('7', 'Basreng Pedas', 'makanan', 25000, 25),
('8', 'Air Mineral 600ml', 'minuman', 5000, 55),
('9', 'Kaus Kaki Sport', 'pakaian', 25000, 15),
('10', 'Biskuit Gandum', 'makanan', 12000, 25),
('11', 'Jus Jeruk Peras', 'minuman', 22000, 18),
('12', 'Kemeja Pendek', 'pakaian', 120000, 8),
('13', 'Mie Instan Cup', 'makanan', 10000, 40),
('14', 'Susu UHT 250ml', 'minuman', 7000, 32),
('15', 'Celana Pendek', 'pakaian', 85000, 14);

create table voucher (
	id int not null auto_increment primary key,
    kode_voucher varchar(50),
    potongan int,
	kuota int
);

insert into voucher
values
('1', 'VOUCHER10', '10000', '9'),
('2', 'VOUCHER20', '20000', '9'),
('3', 'VOUCHER30', '30000', '10');

select * from voucher;

create table transaksi (
	id_transaksi int auto_increment primary key,
    nama_produk varchar(50),
    jumlah_beli int,
    total_akhir int,
    voucher_digunakan varchar(50),
    tanggal_jam datetime default current_timestamp
);

select * from transaksi;

