    // resource 资源router
    resource, err := initResourceController(global.DaprConfig.Mysql)
    if err != nil {
        return err
    }
    resourceRouter := r.Group("/resources"
    resourceRouter.POST("", resource.Create)
    resourceRouter.PUT("/:id", resource.Update)
    resourceRouter.GET("/:id", resource.Get)
    resourceRouter.GET("", resource.List)
    resourceRouter.DELETE("", resource.Delete)

    // role 角色router
    role, err := initRoleController(global.DaprConfig.Mysql)
    if err != nil {
        return err
    }
    roleRouter := r.Group("/roles"
    roleRouter.POST("", role.Create)
    roleRouter.PUT("/:id", role.Update)
    roleRouter.GET("/:id", role.Get)
    roleRouter.GET("", role.List)
    roleRouter.DELETE("", role.Delete)

    // user 用户router
    user, err := initUserController(global.DaprConfig.Mysql)
    if err != nil {
        return err
    }
    userRouter := r.Group("/users"
    userRouter.POST("", user.Create)
    userRouter.PUT("/:id", user.Update)
    userRouter.GET("/:id", user.Get)
    userRouter.GET("", user.List)
    userRouter.DELETE("", user.Delete)

