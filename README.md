# chat-room---socket-programing
در این پروژه ما یک server و چندتا client  داریم که قرار همزمان قرار است به server متصل شوند و به واسطه server در  محیطی یکپارچه بتوانند باهم پیام تبادل کنند. 
                                                                                                                                                          
کارکرد این chat room به این صورت است که هر client ی به server متصل و وارد محیط chat room می شود و          
 server بلافاصه پیام خوش آمد گویی را به کاربر نمایش می دهد و در صفحه عمومی chat room اتصال client را به همه client ها از جمله خود client ی که وارد شده گزارش می دهد و به client  اجازه می دهد پیغام بگزارد. 
در این پروژه ما سه فایل در بر بستر زبان پایتون داریم که هر کدام مسئول بخشی از پروزه است. <
کتابخانه هایی که در این پروژه استفاده شده اند: 
```
import socket
```
این کتابخانه جزء اصلی برنامه است و همه متدهای اصلی و مربوط به شبکه نظیر bind() و coonect() مربوط به این کتابخانه است.
```
import select
```
مدیریت همزمان چندین اتصال یا فایل بدون مسدودسازی (Non-blocking I/O) ،نظارت بر چندین سوکت به صورت همزمان (مثلاً در سرورهای چندکاربره) و جلوگیری از توقف برنامه هنگام انتظار برای ورودی/خروجی . 
```
import re
```
برای پردازش و جستجوی متن با استفاده از عبارات منظم و اعتبارسنجی فرمت دادهها (مانند ایمیل، شماره تلفن) استفاده می شود.
```
import  thearding 
```
برای مدیریت همزمان چند وظیفه انجام می شود و در اینجا برای اتصال همزمان چند client به server و مدیریت همزمان آنها است.
برای تعامل با سیستم و پارامترهای زمان اجرا و در اینجا برای خروج اضطراری در صورت خطای بحرانی از سمت client است که این کتابخانه در با کمک کتابخانه os و دستور های sys.exit(0) و  در برنامه است. <
```
from os import _exit
```
برای خاتمه فوری فرآیند بدون اجرای تمیزکاری با دستور _exit(0) است.
```
from client_customing import Client
```
ما برای server در کلاس Client کتابخانه سوکت را شخصی سازی کردیم و حالا در فایل server کلاس Client درفایل server فراخوانی کردیم.










