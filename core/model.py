
class Paginacao:
    def __int__(self, totalPages, totalElements, pageSize, pageNumber):
        self.totalPages = totalPages
        self.totalElements = totalElements
        self.pageSize = pageSize
        self.pageNumber = pageNumber