import uiautomator2 as u2
import time

# 连接到设备（确保设备已连接并开启了 USB 调试）
d = u2.connect()

d(scrollable=True).scroll.toEnd()
d(resourceId="com.amaze.filemanager:id/pathbar").click()
# d.xpath('//*[@resource-id="com.amaze.filemanager:id/buttons"]/android.widget.ImageButton[2]')
d(resourceId="com.amaze.filemanager:id/lin").child(index = 7).click()
# d(resourceId="com.amaze.filemanager:id/home").click()