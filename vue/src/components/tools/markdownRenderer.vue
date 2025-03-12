<template>
  <div :style="{ textAlign: `start`, overflowY: `auto` }">
    <span v-for="(item, index) in content" :key="index">
      <template v-if="item.type === 'text'">
        <span v-for="(subItem, subIndex) in item.content" :key="subIndex">
          <!-- <span
            v-if="subItem.type === 'orderList'"
            :style="{
              fontWeight: 'bold',
              marginLeft: (subItem.level - 1) * 20 + 'px',
            }"
          >
            <br />  {{ subItem.msg }}
          </span> -->
          <span v-if="subItem.type === 'orderList'">
            <br />
            <span :style="{ marginLeft: (subItem.level - 1) * 20 + 'px' }">{{
              subItem.msg
            }}</span>
          </span>
          <span v-else-if="subItem.type === 'list'">
            <br />
            <span :style="{ marginLeft: (subItem.level - 1) * 20 + 'px' }"
              >•</span
            >
          </span>
          <span v-else-if="subItem.type === 'bold_text'">
            <span :style="{ fontWeight: 'bold' }">{{ subItem.msg }}</span>
          </span>
          <span v-else-if="subItem.type === 'italic_text'">
            <span :style="{ fontStyle: 'italic' }">{{ subItem.msg }}</span>
          </span>
          <span v-else-if="subItem.type === 'link'">
            <a :href="subItem.url" target="_blank">{{ subItem.msg }}</a>
          </span>
          <span v-else-if="subItem.type === 'paragraph'">
            <span>{{ subItem.msg }}</span>
          </span>
          <span v-else-if="subItem.type === 'text'">
            <span>{{ subItem.msg }}</span>
          </span>
          <span v-else-if="subItem.type === 'code'">
            <div class="code-block">
              <pre>{{ subItem.msg }}</pre>
            </div>
          </span>
        </span>
      </template>
      <template v-else-if="item.type === 'table'">
        <table border="1">
          <thead>
            <tr v-for="(row, rowIndex) in item.rows" :key="rowIndex">
              <template v-if="row.type === 'header'">
                <th v-for="(cell, cellIndex) in row.cells" :key="cellIndex">
                  {{ cell }}
                </th>
              </template>
              <template v-else-if="row.type === 'row'">
                <td v-for="(cell, cellIndex) in row.cells" :key="cellIndex">
                  {{ cell }}
                </td>
              </template>
            </tr>
          </thead>
        </table>
      </template>
      <br />
    </span>
  </div>
</template>

<script>
import { markdownParse } from "@/utils/markdownParseJson";
export default {
  props: {
    markdown: {
      type: String,
      default: ``,
    },
  },
  computed: {
    content() {
      // console.log(markdownParse(this.markdown).content);
      return markdownParse(this.markdown).content;
    },
  },
};
</script>

<style scoped>
table {
  width: 100%;
  border-collapse: collapse;
}
th,
td {
  padding: 8px;
  text-align: left;
}
th {
  background-color: #f2f2f2;
}
.code-block {
  background-color: #2d2d2d;
  color: #f8f8f2;
  font-family: "Fira Code", "Courier New", monospace;
  padding: 10px;
  border-radius: 8px;
  overflow-x: auto;
  white-space: pre-wrap;
  word-wrap: break-word;
  border: 1px solid #444;
}
</style>
