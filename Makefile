.PHONY: help dev build test clean docker-up docker-down lint

help: ## نمایش راهنمای دستورات
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

dev: ## اجرای پروژه در محیط توسعه
	docker-compose up -d
	cd frontend && npm run dev & cd backend && go run main.go

build: ## ساخت پروژه
	cd frontend && npm run build
	cd backend && go build -o ma2ta-server

test: ## اجرای تست‌ها
	cd frontend && npm test
	cd backend && go test ./...
	cd mobile && flutter test

clean: ## پاک کردن فایل‌های اضافی
	rm -rf frontend/dist
	rm -rf backend/ma2ta-server
	rm -rf mobile/build
	find . -name "node_modules" -type d -prune -exec rm -rf '{}' +

docker-up: ## راه‌اندازی داکر
	docker-compose up -d

docker-down: ## توقف داکر
	docker-compose down

lint: ## بررسی کیفیت کد
	cd frontend && npm run lint
	cd backend && golangci-lint run
	cd mobile && flutter analyze