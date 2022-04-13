// @title		initResourceController
// @description	初始化资源控制器
// @author		rong	2022/03/03
// @return 	    ResourceController
func initResourceController(mysqlcfg *database.DaprMysqlConfig) (*controllers.ResourceController, error) {
	wire.Build(controllers.ResourceControllerProviderSet, repo.ResourceRepoProviderSet, database.DaprMysqlProviderSet)
	return nil, nil
}

// @title		initRoleController
// @description	初始化角色控制器
// @author		rong	2022/03/03
// @return 	    RoleController
func initRoleController(mysqlcfg *database.DaprMysqlConfig) (*controllers.RoleController, error) {
	wire.Build(controllers.RoleControllerProviderSet, repo.RoleRepoProviderSet, database.DaprMysqlProviderSet)
	return nil, nil
}

// @title		initUserController
// @description	初始化用户控制器
// @author		rong	2022/03/03
// @return 	    UserController
func initUserController(mysqlcfg *database.DaprMysqlConfig) (*controllers.UserController, error) {
	wire.Build(controllers.UserControllerProviderSet, repo.UserRepoProviderSet, database.DaprMysqlProviderSet)
	return nil, nil
}

