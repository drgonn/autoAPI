// @title		initResourceController
// @description	初始化资源控制器
// @author		rong	2022/03/04
// @return 	    ResourceController 资源控制器
//         	    error 错误，无错误为成功
func initResourceController(mysqlcfg *database.DaprMysqlConfig) (*controllers.ResourceController, error) {
	wire.Build(controllers.ResourceControllerProviderSet, repo.ResourceRepoProviderSet, database.DaprMysqlProviderSet)
	return nil, nil
}

// @title		initRoleController
// @description	初始化角色控制器
// @author		rong	2022/03/04
// @return 	    RoleController 角色控制器
//         	    error 错误，无错误为成功
func initRoleController(mysqlcfg *database.DaprMysqlConfig) (*controllers.RoleController, error) {
	wire.Build(controllers.RoleControllerProviderSet, repo.RoleRepoProviderSet, database.DaprMysqlProviderSet)
	return nil, nil
}

// @title		initUserController
// @description	初始化用户控制器
// @author		rong	2022/03/04
// @return 	    UserController 用户控制器
//         	    error 错误，无错误为成功
func initUserController(mysqlcfg *database.DaprMysqlConfig) (*controllers.UserController, error) {
	wire.Build(controllers.UserControllerProviderSet, repo.UserRepoProviderSet, database.DaprMysqlProviderSet)
	return nil, nil
}

