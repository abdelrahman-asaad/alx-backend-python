import asyncio
import aiosqlite  # مكتبة للتعامل مع SQLite بشكل غير متزامن (asynchronous)

# 🔹 دالة أولى: تجيب كل المستخدمين
async def async_fetch_users():
    async with aiosqlite.connect("users.db") as db:
        cursor = await db.execute("SELECT * FROM users")
        results = await cursor.fetchall()
        await cursor.close()
        print("👥 All Users:")
        for row in results:
            print(row)

# 🔹 دالة ثانية: تجيب المستخدمين اللي عمرهم أكبر من 40
async def async_fetch_older_users():
    async with aiosqlite.connect("users.db") as db:
        cursor = await db.execute("SELECT * FROM users WHERE age > 40")
        results = await cursor.fetchall()
        await cursor.close()
        print("\n🧓 Users older than 40:")
        for row in results:
            print(row)

# 🔹 دالة رئيسية لتشغيل الدالتين معًا
async def fetch_concurrently():
    # asyncio.gather بتشغل الدالتين في نفس الوقت (concurrently)
    await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )

# 🔹 تشغيل الـ event loop
if __name__ == "__main__": # to prevent execution when imported as a module , so that the code only runs when the script is executed directly.
    asyncio.run(fetch_concurrently())
