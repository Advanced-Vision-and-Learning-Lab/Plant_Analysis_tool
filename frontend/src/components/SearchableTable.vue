<template>
  <div class="searchable-table-container">
    <!-- Search and Actions Bar -->
    <div class="table-controls">
      <div class="search-container">
        <input
          v-model="searchQuery"
          type="text"
          class="search-input"
          :placeholder="searchPlaceholder"
        />
        <span class="search-icon">🔍</span>
      </div>
      
      <div class="table-actions">
        <ConfigurableButton
          text="Download CSV"
          variant="outline"
          size="small"
          @click="downloadCSV"
        />
        <div class="items-per-page">
          <label>Show:</label>
          <select v-model="itemsPerPage" class="items-select">
            <option value="10">10</option>
            <option value="25">25</option>
            <option value="50">50</option>
            <option value="100">100</option>
          </select>
        </div>
      </div>
    </div>

    <!-- Table -->
    <div class="table-wrapper">
      <table class="data-table">
        <thead>
          <tr>
            <!-- <th 
              v-for="header in headers" 
              :key="header.value"
              @click="sortBy(header.value)"
              :class="{ sortable: header.sortable !== false }"
            > -->
              {{ header.text }}
              <span v-if="header.sortable !== false" class="sort-icon">
                {{ getSortIcon(header.value) }}
              </span>
            </th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(item, index) in paginatedItems" :key="index">
            <td v-for="header in headers" :key="header.value">
              {{ formatCellValue(item[header.value], header) }}
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- No Results Message -->
    <div v-if="filteredItems.length === 0" class="no-results">
      <p>No results found for "{{ searchQuery }}"</p>
    </div>

    <!-- Pagination -->
    <div v-if="totalPages > 1" class="pagination">
      <button 
        class="pagination-btn"
        @click="previousPage"
        :disabled="currentPage === 1"
      >
        ‹ Previous
      </button>
      
      <div class="page-numbers">
        <button 
          v-for="page in visiblePages" 
          :key="page"
          class="page-btn"
          :class="{ active: page === currentPage }"
          @click="goToPage(page)"
        >
          {{ page }}
        </button>
      </div>
      
      <button 
        class="pagination-btn"
        @click="nextPage"
        :disabled="currentPage === totalPages"
      >
        Next ›
      </button>
    </div>

    <!-- Results Summary -->
    <div class="results-summary">
      <span>
        Showing {{ startIndex + 1 }}-{{ endIndex }} of {{ filteredItems.length }} results
      </span>
    </div>
  </div>
</template>

<script>
import ConfigurableButton from './ConfigurableButton.vue'

export default {
  name: 'SearchableTable',
  components: {
    ConfigurableButton
  },
  props: {
    headers: {
      type: Array,
      required: true,
      default: () => []
    },
    items: {
      type: Array,
      required: true,
      default: () => []
    },
    searchPlaceholder: {
      type: String,
      default: 'Search...'
    },
    defaultSort: {
      type: String,
      default: null
    },
    defaultSortDirection: {
      type: String,
      default: 'asc',
      validator: value => ['asc', 'desc'].includes(value)
    }
  },
  
  data() {
    return {
      searchQuery: '',
      currentPage: 1,
      itemsPerPage: 25,
      // sortBy: this.defaultSort,
      sortDirection: this.defaultSortDirection
    };
  },
  
  computed: {
    filteredItems() {
      if (!this.searchQuery) {
        return this.items;
      }
      
      const query = this.searchQuery.toLowerCase();
      return this.items.filter(item => {
        return this.headers.some(header => {
          const value = item[header.value];
          if (value == null) return false;
          return value.toString().toLowerCase().includes(query);
        });
      });
    },
    
    // sortedItems() {
    //   if (!this.sortBy) {
    //     return this.filteredItems;
    //   }
      
    //   return [...this.filteredItems].sort((a, b) => {
    //     const aVal = a[this.sortBy];
    //     const bVal = b[this.sortBy];
        
    //     // Handle null/undefined values
    //     if (aVal == null && bVal == null) return 0;
    //     if (aVal == null) return 1;
    //     if (bVal == null) return -1;
        
    //     // Handle numeric values
    //     if (typeof aVal === 'number' && typeof bVal === 'number') {
    //       return this.sortDirection === 'asc' ? aVal - bVal : bVal - aVal;
    //     }
        
    //     // Handle string values
    //     const aStr = aVal.toString().toLowerCase();
    //     const bStr = bVal.toString().toLowerCase();
        
    //     if (this.sortDirection === 'asc') {
    //       return aStr.localeCompare(bStr);
    //     } else {
    //       return bStr.localeCompare(aStr);
    //     }
    //   });
    // },
    
    totalPages() {
      return Math.ceil(this.sortedItems.length / this.itemsPerPage);
    },
    
    paginatedItems() {
      const start = (this.currentPage - 1) * this.itemsPerPage;
      const end = start + this.itemsPerPage;
      return this.sortedItems.slice(start, end);
    },
    
    startIndex() {
      return (this.currentPage - 1) * this.itemsPerPage;
    },
    
    endIndex() {
      return Math.min(this.startIndex + this.itemsPerPage, this.sortedItems.length);
    },
    
    visiblePages() {
      const pages = [];
      const maxVisible = 5;
      
      if (this.totalPages <= maxVisible) {
        for (let i = 1; i <= this.totalPages; i++) {
          pages.push(i);
        }
      } else {
        let start = Math.max(1, this.currentPage - Math.floor(maxVisible / 2));
        let end = Math.min(this.totalPages, start + maxVisible - 1);
        
        if (end - start + 1 < maxVisible) {
          start = Math.max(1, end - maxVisible + 1);
        }
        
        for (let i = start; i <= end; i++) {
          pages.push(i);
        }
      }
      
      return pages;
    }
  },
  
  watch: {
    searchQuery() {
      this.currentPage = 1;
    },
    
    itemsPerPage() {
      this.currentPage = 1;
    }
  },
  
  methods: {
    // sortBy(column) {
    //   if (this.sortBy === column) {
    //     this.sortDirection = this.sortDirection === 'asc' ? 'desc' : 'asc';
    //   } else {
    //     // this.sortBy = column;
    //     this.sortDirection = 'asc';
    //   }
    // },
    
    // getSortIcon(column) {
    //   if (this.sortBy !== column) {
    //     return '↕';
    //   }
    //   return this.sortDirection === 'asc' ? '↑' : '↓';
    // },
    
    formatCellValue(value, header) {
      if (value == null) return '-';
      
      // Apply custom formatter if provided
      if (header.formatter && typeof header.formatter === 'function') {
        return header.formatter(value);
      }
      
      // Format numbers
      if (typeof value === 'number') {
        if (header.decimals !== undefined) {
          return value.toFixed(header.decimals);
        }
        return value.toLocaleString();
      }
      
      return value.toString();
    },
    
    previousPage() {
      if (this.currentPage > 1) {
        this.currentPage--;
      }
    },
    
    nextPage() {
      if (this.currentPage < this.totalPages) {
        this.currentPage++;
      }
    },
    
    goToPage(page) {
      this.currentPage = page;
    },
    
    downloadCSV() {
      const headers = this.headers.map(h => h.text);
      const csvContent = [
        headers.join(','),
        ...this.sortedItems.map(item => 
          headers.map(header => {
            const headerObj = this.headers.find(h => h.text === header);
            const value = item[headerObj.value];
            const formattedValue = this.formatCellValue(value, headerObj);
            // Escape commas and quotes in CSV
            return `"${formattedValue.replace(/"/g, '""')}"`;
          }).join(',')
        )
      ].join('\n');
      
      const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
      const link = document.createElement('a');
      const url = URL.createObjectURL(blob);
      link.setAttribute('href', url);
      link.setAttribute('download', 'table_data.csv');
      link.style.visibility = 'hidden';
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    }
  }
};
</script>

<style scoped>
.searchable-table-container {
  width: 100%;
  background: rgba(255, 255, 255, 0.08);
  border-radius: 12px;
  overflow: hidden;
}

.table-controls {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px;
  background: rgba(255, 255, 255, 0.1);
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.search-container {
  position: relative;
  flex: 1;
  max-width: 300px;
}

.search-input {
  width: 100%;
  padding: 8px 12px 8px 36px;
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: 6px;
  background: rgba(255, 255, 255, 0.1);
  color: white;
  font-size: 14px;
  outline: none;
}

.search-input::placeholder {
  color: rgba(255, 255, 255, 0.6);
}

.search-icon {
  position: absolute;
  left: 12px;
  top: 50%;
  transform: translateY(-50%);
  color: rgba(255, 255, 255, 0.6);
  font-size: 14px;
}

.table-actions {
  display: flex;
  align-items: center;
  gap: 16px;
}

.items-per-page {
  display: flex;
  align-items: center;
  gap: 8px;
  color: white;
  font-size: 14px;
}

.items-select {
  padding: 4px 8px;
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: 4px;
  background: rgba(255, 255, 255, 0.1);
  color: white;
  font-size: 14px;
  outline: none;
}

.table-wrapper {
  overflow-x: auto;
}

.data-table {
  width: 100%;
  border-collapse: collapse;
  color: white;
}

.data-table th {
  background: rgba(255, 255, 255, 0.1);
  padding: 12px 16px;
  text-align: left;
  font-weight: 600;
  border-bottom: 2px solid rgba(255, 255, 255, 0.2);
  position: relative;
}

.data-table th.sortable {
  cursor: pointer;
  user-select: none;
}

.data-table th.sortable:hover {
  background: rgba(255, 255, 255, 0.15);
}

.sort-icon {
  margin-left: 8px;
  font-size: 12px;
  opacity: 0.7;
}

.data-table td {
  padding: 12px 16px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.data-table tbody tr:hover {
  background: rgba(255, 255, 255, 0.05);
}

.no-results {
  padding: 40px 20px;
  text-align: center;
  color: rgba(255, 255, 255, 0.6);
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 16px;
  padding: 16px 20px;
  background: rgba(255, 255, 255, 0.05);
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.pagination-btn {
  padding: 8px 12px;
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: 6px;
  background: rgba(255, 255, 255, 0.1);
  color: white;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.2s ease;
}

.pagination-btn:hover:not(:disabled) {
  background: rgba(255, 255, 255, 0.2);
}

.pagination-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.page-numbers {
  display: flex;
  gap: 4px;
}

.page-btn {
  padding: 8px 12px;
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: 6px;
  background: rgba(255, 255, 255, 0.1);
  color: white;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.2s ease;
  min-width: 40px;
}

.page-btn:hover {
  background: rgba(255, 255, 255, 0.2);
}

.page-btn.active {
  background: rgba(79, 172, 254, 0.3);
  border-color: rgba(79, 172, 254, 0.5);
}

.results-summary {
  padding: 12px 20px;
  text-align: center;
  color: rgba(255, 255, 255, 0.7);
  font-size: 14px;
  background: rgba(255, 255, 255, 0.05);
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

/* Responsive Design */
@media (max-width: 768px) {
  .table-controls {
    flex-direction: column;
    gap: 16px;
    align-items: stretch;
  }
  
  .search-container {
    max-width: none;
  }
  
  .table-actions {
    justify-content: space-between;
  }
  
  .data-table th,
  .data-table td {
    padding: 8px 12px;
    font-size: 14px;
  }
  
  .pagination {
    flex-direction: column;
    gap: 12px;
  }
  
  .page-numbers {
    order: -1;
  }
}
</style> 