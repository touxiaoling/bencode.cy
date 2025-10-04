
cdef _bdecode(const unsigned char[:] encoded, int bytes_len)

cdef int _parse_forward(int till_char,const unsigned char[:] encoded,int pos,int bytes_len )