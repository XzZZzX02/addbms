<template>
  <div>
    <!-- 添加标题 -->
    <div class="header-title">生成式人工智能多模态内容识别系统</div>

    <div class="container">
      <el-row class="mb-20">
        <el-col :span="24">
          <!-- 上传文件夹按钮 -->
          <input
            type="file"
            ref="fileInput"
            multiple
            webkitdirectory
            @change="handleUpFiles"
            style="display: none"
          />
          <!-- 使用 Element Plus 的 ElButton 设置蓝色背景 -->
          <el-button
            @click="triggerFileInput"
            type="primary"
            class="upload-btn"
          >
            上传文件夹
          </el-button>
        </el-col>
      </el-row>

      <!-- 表格 -->
      <el-table :data="pagedData" class="table" border layout="fixed">
        <el-table-column label="ID" prop="id"></el-table-column>
        <el-table-column label="类型" prop="type"></el-table-column>
        <el-table-column label="文件名" prop="filename"></el-table-column>
        <el-table-column label="详细信息" prop="details"></el-table-column>
        <el-table-column label="操作" align="center">
          <template v-slot="scope">
            <!-- 删除按钮 -->
            <el-button
              size="mini"
              type="danger"
              @click="handleDelete(scope.row)"
            >
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
      <el-pagination
        :current-page="currentPage"
        :page-size="pageSize"
        :total="tableData.length"
        @current-change="handlePageChange"
        layout="prev, pager, next, jumper, ->, total"
      />
    </div>
  </div>
</template>

<script>
import {
  ElButton,
  ElTable,
  ElTableColumn,
  ElRow,
  ElCol,
  ElPagination,
} from "element-plus";
import axios from "axios";

export default {
  name: "App",
  components: {
    ElButton,
    ElTable,
    ElTableColumn,
    ElRow,
    ElCol,
    ElPagination,
  },
  data() {
    return {
      tableData: [], // 表格数据
      currentPage: 1, // 当前页码
      pageSize: 10, // 每页条数
    };
  },
  computed: {
    // 当前页面数据
    pagedData() {
      if (!this.tableData || this.tableData.length === 0) return [];
      const start = (this.currentPage - 1) * this.pageSize;
      const end = start + this.pageSize;
      return this.tableData.slice(start, end);
    },
  },
  methods: {
    // 触发 input 点击事件，打开文件选择框
    triggerFileInput() {
      this.$refs.fileInput.click();
    },

    // 处理文件夹上传
    async handleUpFiles(event) {
      event.preventDefault(); // 阻止默认表单提交行为
      try {
        const files = event.target.files;
        const formData = new FormData();

        // 遍历选中的文件
        for (let i = 0; i < files.length; i++) {
          formData.append("files", files[i]);
        }

        // 发送上传请求
        const response = await axios.post(
          "http://localhost:5000/api/upload-folder",
          formData,
          {
            headers: {
              "Content-Type": "multipart/form-data",
            },
          }
        );

        // 假设后端返回的 all_records 是数组格式
        const records = response.data.all_records;

        // 更新表格数据，处理文件名（去除路径和后缀）
        this.tableData = records.map((record, index) => {
          const filePath = record[2]; // 假设 record[2] 是文件路径和名称
          const fileName = this.extractFileName(filePath); // 处理文件名

          return {
            id: index + 1, // 自动生成 ID
            type: record[1], // 第二项为类型
            filename: fileName, // 处理后的文件名
            details: record[3], // 第四项为详细信息
          };
        });

        this.$message.success("上游文件处理成功！");
      } catch (error) {
        console.error("上传失败:", error);
        this.$message.error("上传失败，请重试");
      }
    },

    // 删除记录
    async handleDelete(row) {
      try {
        // 发送删除请求
        const response = await axios.post(
          "http://localhost:5000/api/delete-record",
          { id: row.id }
        );

        // 判断请求是否成功
        if (
          response.data.success &&
          Array.isArray(response.data.remaining_records)
        ) {
          // 直接使用后端返回的数据
          this.tableData = response.data.remaining_records.map((record) => {
            const filePath = record[2]; // 假设 record[2] 是文件路径和名称
            const fileName = this.extractFileName(filePath); // 处理文件名

            return {
              id: record[0], // 元组第 1 项为 id
              type: record[1], // 元组第 2 项为类型
              filename: fileName, // 处理后的文件名
              details: record[3], // 元组第 4 项为详细信息
            };
          });

          this.$message.success("删除成功");
        } else {
          this.$message.error(response.data.error || "删除失败，数据格式异常");
        }
      } catch (error) {
        console.error("删除失败:", error);
        this.$message.error("删除失败，请稍后重试");
      }
    },

    // 提取文件的基本名称，不包括路径和扩展名
    extractFileName(filePath) {
      // 获取文件名，不包括路径和后缀
      const fileNameWithExtension = filePath.split("\\").pop().split("/").pop(); // 支持 Windows 和 Unix 路径分隔符
      return fileNameWithExtension.replace(/\.[^/.]+$/, ""); // 去掉文件扩展名
    },

    // 翻页事件处理
    handlePageChange(newPage) {
      this.currentPage = newPage;
    },
  },
};
</script>

<style scoped>
/* 标题区域样式 */
.header-title {
  text-align: center; /* 居中显示 */
  font-size: 50px; /* 设置大字的字体大小 */
  font-weight: bold; /* 字体加粗 */
  color: #333; /* 设置字体颜色 */
  padding: 20px; /* 增加上下内边距，确保标题不紧贴页面边缘 */
  background-color: #f5f5f5; /* 背景颜色 */
  margin: 0; /* 去除外边距 */
}

/* 容器，增加左右内边距 */
.container {
  padding: 20px;
  margin: 0 auto;
  max-width: 1200px; /* 设置表格的最大宽度 */
}

/* 表格整体样式 */
.el-table {
  margin-top: 20px;
  border: 1px solid #ccc; /* 加粗表格四周边框，宽度为6px */
  border-collapse: separate; /* 防止内边框重叠 */
  border-radius: 10px; /* 让表格四周的边角圆滑 */
}

.el-table th,
.el-table td {
  border: 1px solid #ccc; /* 单元格边框保持为1px，不加粗 */
  font-size: 18px; /* 放大单元格文字 */
}

/* 表头样式 */
.el-table th,
.el-table th div {
  background-color: #fff !important; /* 恢复表头背景为白色 */
  color: #000 !important; /* 恢复表头文字为黑色 */
  font-size: 20px; /* 表头文字放大 */
  font-weight: bold; /* 表头文字加粗 */
  text-align: center; /* 表头文字居中 */
}

/* 按钮样式 */
.el-button {
  font-size: 18px; /* 按钮文字放大 */
}

.el-button--primary {
  background-color: #409eff; /* 设置为蓝色 */
  border-color: #409eff; /* 设置蓝色边框 */
}

.el-button--primary:hover {
  background-color: #66b1ff; /* 悬停时背景颜色变浅 */
  border-color: #66b1ff;
}

/* 增加右侧边框的加粗 */
.el-table::after {
  content: "";
  position: absolute;
  right: 0;
  top: 0;
  bottom: 0;
  width: 6px;
  background-color: #ccc; /* 设置右侧边框颜色 */
}
</style>