from __future__ import division 
from struct import pack, unpack
class Compresor:
    def encodearNumero(self,num):
        """Variable byte code encode number.
        Usage:
        import vbcode
        vbcode.encode_number(128)
        """
        self.byteArray = []
        while True:
            self.byteArray.insert(0, num % 128)
            if num < 128:
                break
            num = num // 128
        self.byteArray[-1] += 128
        return pack('%dB' % len(self.byteArray), *self.byteArray)

    def encodear(self,nums):
        byteArray = []
        for num in nums:
            byteArray.append(self.encodearNumero(num))
        return b"".join(byteArray)

    def decodear(self,byteArray):
        self.n = 0
        self.nums = []
        byteArray = unpack('%dB' % len(byteArray), byteArray)
        for byte in byteArray:
            if byte < 128:
                self.n = 128 * self.n + byte
            else:
                self.n = 128 * self.n + (byte - 128)
                self.nums.append(self.n)
                self.n = 0
        return self.nums
