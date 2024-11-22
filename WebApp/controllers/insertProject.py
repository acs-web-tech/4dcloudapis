def insertProject(request,connection,id):
    token = request.headers.get("4dcloud-auth-token")
    cursor = connection["4dapis"]["clients"]
    cursor.update_one({"secrets":token},{"$push":{"projects":{"id":id["projectname"]}}})