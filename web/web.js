/** 上传文件
要使用 PHP 上传文件，首先要保证 php.ini 文件中
file_uploads=On

参考博客：
http://www.cnblogs.com/thenbsp/archive/2011/07/15/2107503.html
http://blog.p2hp.com/archives/2924

<form action="upload.php"  method="post"  enctype="multipart/form-data">
  <input type="hidden" name="MAX_FILE_SIZE" value="1000000">
  选择文件：<input type="file" name="myfile">
  <input type="submit" name="submit" value="上传文件">
</form>

注意几个特征属性:
POST方法:
表单最常用的功能，向目标页面传递变量，
我们在上传文件的时候，会在表单中设置相应的属性，来完成文件的传递

enctype="multipart/form-data"
这样服务器就会知道，我们要传递一个文件，
这样服务器可以知道上载的文件带有常规的表单信息。

MAX_FILE_SIZE
此字段必须在文件输入字段之前，控制最大的传递文件的大小(字节)

<input type="file" name="userfile">
设置浏览器文件输入浏览按钮

在 PHP 代码中有两个重要的变量 $_POST 和 $_FILES
$_POST['submit'] 中的参数名对应 <input type="submit" ...> 中的 name 值
$_FILES['myfile'] 中的参数名对应 <input type="file" ...> 中的 name 值
注意这一点，否则 PHP 代码将会出现类似 Undefined index 的问题
 */

// 如果把 '.slideshow img' 放到前面就出错，是不是因为有 .slideshow 和 img 两个标签？？？
$('body').on('click', '.slideshow img', function(e) {
		slideShow($(this), e.pageX)
});

// jQuery 的 offset() 可以获得元素相对于 document 的位置信息，通常可以说是这个元素的坐标值
$('#p_books .book').offset()

// scrollTop() 方法返回或设置匹配元素的滚动条的垂直位置。
// offset (可选) 指的是滚动条相对于其顶部的偏移。
// 如果该方法未设置参数，则返回以像素计的相对滚动条顶部的偏移。
// 该方法对于可见元素和不可见元素均有效。
// 当用于获取值时，该方法只返回第一个匹配元素的 scroll top offset
$(selector).scrollTop(offset)

// animate() 是jQuery 的一个特效函数方法，animate()方法执行 CSS 属性集的自定义动画
// 该方法通过 CSS 样式将元素从一个状态改为另一个状态
// 回到 id 为 comments 的位置
$('html,body').animate({scrollTop:$('#comments').offset().top}, 800);
// 获得元素 bottom
$('#comments').offset() + $('#comments').height()
// 获得屏幕窗口高度
$(window).height()

// 调用某个方法时，传入的 $(this) 指向调用这个方法的元素
$('#comments').slideUp('slow', function() {
	assert($(this) === $('#comments'))
})

// 通过HTTP请求加载远程数据
// $.ajax()返回其创建的XMLHttpRequest对象
// $.ajax()只有一个参数：参数key/value对象，包含各配置及回调函数信息
$.ajax({
  			cache: false,
  			type: "GET",
        dataType: "html",
  			url: "/luminocity/book_info.php", //请求的HTML页面的URL地址
  			data: "book="+hashes[1]+"&type="+hashes[2],
  			success: function(resultdata) {
  			  // 请求成功后的回调函数，两个参数：服务器返回数据，返回状态
          var thissection = $(".description");
          thissection.html(resultdata);
  			}
		});

// ???????
// jQuery 的 slideUp({ duration: 300, easing: "easeInOutQuad", complete: function(){...}) 为什么没用
// 改成 slideUp('slow', function(){...}) 就有用了
