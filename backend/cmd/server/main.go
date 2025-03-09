package main

import (
    "log"
    "github.com/gin-gonic/gin"
    "github.com/galleryartma2ta/Ma2tA/backend/config"
    "github.com/galleryartma2ta/Ma2tA/backend/routes"
    "github.com/galleryartma2ta/Ma2tA/backend/middleware"
)

func main() {
    // تنظیمات اولیه
    config.LoadEnv()
    db := config.InitDB()
    redis := config.InitRedis()

    // راه‌اندازی Gin
    r := gin.Default()

    // میدلور‌ها
    r.Use(middleware.CORS())
    r.Use(middleware.Auth())
    r.Use(middleware.RateLimit(redis))

    // مسیرها
    routes.SetupRoutes(r, db)

    // شروع سرور
    log.Fatal(r.Run(":8080"))
}