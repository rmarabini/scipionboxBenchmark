sync
for DISK in /dev/sd?
do
echo $DISK
echo 3 > /proc/sys/vm/drop_caches
blockdev --flushbufs $DISK
hdparm -F $DISK
done

#Explanation:

#sync: From the man page: flush file system buffers. Force changed blocks to disk, update the super block.

#echo 3 > /proc/sys/vm/drop_cache: from the kernel docs this will cause the kernel to drop clean caches

#blockdev --flushbufs /dev/sda: from the man page: call block device ioctls [to] flush buffers.

#hdparm -F /dev/sda: from the man page: Flush the on-drive write cache buffer (older drives may not implement this)

#Although the blockdev and hdparm commands look similar according to an answer above they issue different ioctls to the device. 
