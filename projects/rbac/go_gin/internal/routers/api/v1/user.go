package v1
type User struct{}
func NewUser() User{return User{}}

func (p User) Create(c *gin.Context) {
param := service.CreateUserRequest{}
response := app.NewResponse(c)
valid, errs := app.BindAndValid(c, &param)
if !valid {
    global.Logger.Errorf("app.BindAndValid errs: %v", errs)
    errRsp := errcode.InvalidParams.WithDetails(errs.Errors()...)
    response.ToErrorResponse(errRsp)
    return
}
    svc := service.New(c.Request.Context())
user_id, err := svc.CreateUser(&param)
if err != nil {
global.Logger.Errorf("svc.CreateUser err: %v", err)
if user_id == 0 {
	response.ToErrorResponse(errcode.ErrorCreateUserNameExisted)
} else {
	response.ToErrorResponse(errcode.ErrorCreateUserFail)
}
return
}
param.Id = user_id
response.ToResponse(param)
return
}
func (t User) Get(c *gin.Context) {
	param := service.GetUserRequest{Id: convert.StrTo(c.Param("id")).MustUInt32()}
	response := app.NewResponse(c)
	valid, errs := app.BindAndValid(c, &param)
	if !valid {
		global.Logger.Errorf("app.BindAndValid errs: %v", errs)
		response.ToErrorResponse(errcode.InvalidParams.WithDetails(errs.Errors()...))
		return
	}
	svc := service.New(c.Request.Context())
	user, err := svc.GetUser(&param)
	if err != nil {
		global.Logger.Errorf("svc.GetUser err: %v", err)
		response.ToErrorResponse(errcode.ErrorGetUserFail)
		return
	}
	response.ToResponse(user)
	return
}

func (t User) List(c *gin.Context) {
	param := service.UserListRequest{}
	response := app.NewResponse(c)
	valid, errs := app.BindAndValid(c, &param)
	if !valid {
		global.Logger.Errorf("app.BindAndValid errs: %v", errs)
		errRsp := errcode.InvalidParams.WithDetails(errs.Errors()...)
		response.ToErrorResponse(errRsp)
		return
	}

	svc := service.New(c)
	pager := app.Pager{
		Page:     app.GetPage(c),
		PageSize: app.GetPageSize(c),
	}
	totalRows, err := svc.CountUser(&service.CountUserRequest{
        Uid: param.Uid,
	})
	if err != nil {
		global.Logger.Errorf("svc.CountUser err: %v", err)
		response.ToErrorResponse(errcode.ErrorCountUserFail)
	}
	users, err := svc.GetUserList(&param, &pager)
	if err != nil {
		global.Logger.Errorf("svc.GetUserList err: %v", err)
		response.ToErrorResponse(errcode.ErrorGetUserListFail)
		return
	}
	response.ToResponseList(users, totalRows)
	return
}

func (t User) Update(c *gin.Context) {
	param := service.UpdateUserRequest{Id: convert.StrTo(c.Param("id")).MustUInt32()}
	response := app.NewResponse(c)
	valid, errs := app.BindAndValid(c, &param)
	if !valid {
		global.Logger.Errorf("app.BindAndValid errs: %v", errs)
		response.ToErrorResponse(errcode.InvalidParams.WithDetails(errs.Errors()...))
		return
	}

	svc := service.New(c.Request.Context())
	n, err := svc.UpdateUser(&param)
	if err != nil || n < 1 {
		global.Logger.Errorf("svc.UpdateUser err: %v", err)
		response.ToErrorResponse(errcode.ErrorUpdateUserFail)
		return
	}

	response.ToResponse(gin.H{})
	return
}

func (t User) Delete(c *gin.Context) {
	param := service.DeleteUserRequest{Id: convert.StrTo(c.Param("id")).MustUInt32()}
	response := app.NewResponse(c)
	valid, errs := app.BindAndValid(c, &param)
	if !valid {
		global.Logger.Errorf("app.BindAndValid errs: %v", errs)
		response.ToErrorResponse(errcode.InvalidParams.WithDetails(errs.Errors()...))
		return
	}

	svc := service.New(c.Request.Context())
	n, err := svc.DeleteUser(&param)
	if err != nil || n < 1{
		global.Logger.Errorf("svc.DeleteUser err: %v", err)
		response.ToErrorResponse(errcode.ErrorDeleteUserFail)
		return
	}

	response.ToResponse(gin.H{})
	return
}
