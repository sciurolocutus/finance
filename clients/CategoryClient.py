import requests

class CategoryClient:
    def __init__(self, baseurl, jwt):
        self.baseurl = baseurl + '/categories'
        self.jwt = jwt

    def getCategories(self):
        return requests.get("{0}".format(self.baseurl))

    def getCategory(self, categoryId):
        return requests.get("{0}/{1}".format(self.baseurl, categoryId))

    def deleteCategory(self, categoryId):
        headers={'Authorization': 'JWT ' + self.jwt}
        return requests.delete("{0}/{1}".format(self.baseurl, categoryId), headers=headers)

    def putCategory(self, categoryId, category):
        headers={'Authorization': 'JWT ' + self.jwt}
        return requests.put("{0}/{1}".format(self.baseurl, categoryId), headers=headers, json=category)

    def postCategory(self, category):
        headers={'Authorization': 'JWT ' + self.jwt}
        return requests.post("{0}".format(self.baseurl), headers=headers, json=category)
