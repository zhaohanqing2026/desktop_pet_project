# 电脑桌宠陪伴程序
5人小组GitHub协作实验项目，PySide6实现悬浮透明桌面宠物，支持自动行走、鼠标拖拽、右键交互、多主题。
## 本地运行步骤
1. 打开PowerShell，进入项目根目录 desktop_pet_project
2. 新建虚拟环境
py -m venv .venv
.\.venv\Scripts\activate
3. 安装依赖
pip install -r requirements.txt
4. 启动程序
py main.py
## 协作规则
1. 组长维护 main.py、ui/pet_window.py、requirements.txt、README.md
2. 4位组员仅修改data文件夹内分配文件，禁止改动ui、main.py
3. 流程：Fork仓库 → 创建个人任务分支 → 修改指定data文件 → 本地运行测试 → commit+push → 提交PR等待组长Review合并
## 仓库提交证据
1. 4条Issue任务截图
2. 4份Pull Request页面截图
3. 组长Review评论记录截图
4. 程序运行最终GUI截图