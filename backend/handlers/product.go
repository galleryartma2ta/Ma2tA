func GetProducts(c *gin.Context) {
    // برای گذاشتن breakpoint، روی خط کلیک کنید
    products, err := db.GetAllProducts()
    if err != nil {
        // اینجا breakpoint بگذارید
        c.JSON(500, gin.H{"error": err.Error()})
        return
    }
    c.JSON(200, products)
}