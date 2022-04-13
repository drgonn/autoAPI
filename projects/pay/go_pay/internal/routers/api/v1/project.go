package v1
type Project struct{}
func NewProject() Project{return Project{}}

func (p Project) Create(c *gin.Context) {
param := service.CreateProjectRequest{}
response := app.NewResponse(c)
valid, errs := app.BindAndValid(c, &param)
if !valid {
    global.Logger.Errorf("app.BindAndValid errs: %v", errs)
    errRsp := errcode.InvalidParams.WithDetails(errs.Errors()...)
    response.ToErrorResponse(errRsp)
    return
}
    svc := service.New(c.Request.Context())
project_id, err := svc.CreateProject(&param)
if err != nil {
global.Logger.Errorf("svc.CreateProject err: %v", err)
if project_id == 0 {
	response.ToErrorResponse(errcode.ErrorCreateProjectNameExisted)
} else {
	response.ToErrorResponse(errcode.ErrorCreateProjectFail)
}
return
}
param.Id = project_id
response.ToResponse(param)
return
}
func (t Project) Get(c *gin.Context) {
	param := service.GetProjectRequest{Puid: c.Param("puid")}
	response := app.NewResponse(c)
	valid, errs := app.BindAndValid(c, &param)
	if !valid {
		global.Logger.Errorf("app.BindAndValid errs: %v", errs)
		response.ToErrorResponse(errcode.InvalidParams.WithDetails(errs.Errors()...))
		return
	}
	svc := service.New(c.Request.Context())
	project, err := svc.GetProject(&param)
	if err != nil {
		global.Logger.Errorf("svc.GetProject err: %v", err)
		response.ToErrorResponse(errcode.ErrorGetProjectFail)
		return
	}
	response.ToResponse(project)
	return
}

func (t Project) List(c *gin.Context) {
	param := service.ProjectListRequest{}
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
	totalRows, err := svc.CountProject(&service.CountProjectRequest{
        Name: param.Name,
        Puid: param.Puid,
        Ouid: param.Ouid,
        Describe: param.Describe,
	})
	if err != nil {
		global.Logger.Errorf("svc.CountProject err: %v", err)
		response.ToErrorResponse(errcode.ErrorCountProjectFail)
	}
	projects, err := svc.GetProjectList(&param, &pager)
	if err != nil {
		global.Logger.Errorf("svc.GetProjectList err: %v", err)
		response.ToErrorResponse(errcode.ErrorGetProjectListFail)
		return
	}
	response.ToResponseList(projects, totalRows)
	return
}

func (t Project) Update(c *gin.Context) {
	param := service.UpdateProjectRequest{Puid: c.Param("puid")}
	response := app.NewResponse(c)
	valid, errs := app.BindAndValid(c, &param)
	if !valid {
		global.Logger.Errorf("app.BindAndValid errs: %v", errs)
		response.ToErrorResponse(errcode.InvalidParams.WithDetails(errs.Errors()...))
		return
	}

	svc := service.New(c.Request.Context())
	n, err := svc.UpdateProject(&param)
	if err != nil || n < 1 {
		global.Logger.Errorf("svc.UpdateProject err: %v", err)
		response.ToErrorResponse(errcode.ErrorUpdateProjectFail)
		return
	}

	response.ToResponse(gin.H{})
	return
}

func (t Project) Delete(c *gin.Context) {
	param := service.DeleteProjectRequest{Puid: c.Param("puid")}
	response := app.NewResponse(c)
	valid, errs := app.BindAndValid(c, &param)
	if !valid {
		global.Logger.Errorf("app.BindAndValid errs: %v", errs)
		response.ToErrorResponse(errcode.InvalidParams.WithDetails(errs.Errors()...))
		return
	}

	svc := service.New(c.Request.Context())
	n, err := svc.DeleteProject(&param)
	if err != nil || n < 1{
		global.Logger.Errorf("svc.DeleteProject err: %v", err)
		response.ToErrorResponse(errcode.ErrorDeleteProjectFail)
		return
	}

	response.ToResponse(gin.H{})
	return
}
