# 🧪 Manual Testing Checklist for Gestão Tattoo Studio

This checklist provides a comprehensive guide for manual testing of all system functionalities. Use this to validate that everything works as expected from a user perspective.

## 📋 Pre-Testing Setup

- [ ] **Load Test Data**: Run `python tests/test_data.py` to populate the system with test data
- [ ] **Start Application**: Run `python app.py` or `python run.py`
- [ ] **Open Browser**: Navigate to `http://localhost:5000`
- [ ] **Check Date**: Ensure system shows current date correctly

---

## 🏠 Main Dashboard Tests

### Index Page
- [ ] **Page loads correctly** - No errors, proper styling
- [ ] **Navigation menu works** - All menu items clickable
- [ ] **Title and favicon display** - Check browser tab
- [ ] **Responsive design** - Test on different screen sizes

---

## 📅 Sessions Module Tests

### Session Listing (`/sessoes/`)
- [ ] **Page loads without errors**
- [ ] **Sessions display correctly** - Data shows in table format
- [ ] **Search functionality works** - Try searching by client name
- [ ] **Date filter works** - Filter by date range
- [ ] **Action buttons visible** - Edit, Delete, Complete, Limbo options

### Create New Session (`/sessoes/nova`)
- [ ] **Form loads correctly**
- [ ] **All fields present** - Client, Artist, Date, Time, Value, Observations
- [ ] **Artist dropdown populated** - Shows available artists
- [ ] **Date picker works** - Calendar widget functions
- [ ] **Time picker works** - Time selection functions
- [ ] **Form validation works** - Try submitting empty form
- [ ] **Success message appears** - After successful submission
- [ ] **Session appears in list** - Check sessions page

### Session Actions
- [ ] **Edit session works** - Modify existing session
- [ ] **Delete session works** - Remove session (with confirmation)
- [ ] **Complete session works** - Mark as completed, redirects to payment
- [ ] **Send to limbo works** - Move session to limbo
- [ ] **Return from limbo works** - Move session back from limbo
- [ ] **Delete from limbo works** - Remove session from limbo

### Session History (`/sessoes/historico`)
- [ ] **History page loads**
- [ ] **Completed sessions show** - Sessions marked as completed
- [ ] **Data integrity** - All session data preserved
- [ ] **Edit history works** - Can modify historical sessions
- [ ] **Delete history works** - Can remove from history

---

## 💰 Financial Module Tests

### Payments (`/financeiro/`)
- [ ] **Main page loads**
- [ ] **Payments list displays** - All payments in table
- [ ] **Payment totals correct** - Summary calculations accurate
- [ ] **Filter by payment method** - Test different payment types
- [ ] **Date range filter** - Filter payments by date

### Register Payment (`/financeiro/registrar`)
- [ ] **Form loads correctly**
- [ ] **All fields present** - Date, Value, Payment Method, Client, Artist, Description
- [ ] **Payment method dropdown** - Shows all options
- [ ] **Value field accepts decimals** - Test with cents
- [ ] **Form validation works** - Required fields check
- [ ] **Success message appears** - After successful registration
- [ ] **Payment appears in list** - Check payments page
- [ ] **Commission calculated** - If applicable

### Payment Actions
- [ ] **Edit payment works** - Modify existing payment
- [ ] **Delete payment works** - Remove payment (with confirmation)
- [ ] **Payment linked to session** - If created from session completion

---

## 📊 Reports and Extracts Tests

### Monthly Extract (`/extrato/`)
- [ ] **Extract page loads**
- [ ] **Month/year selector works** - Can select different months
- [ ] **Data displays correctly** - Payments and sessions for selected month
- [ ] **Totals calculate correctly** - Summary values accurate
- [ ] **Export functionality** - If available

### Extract Data (`/extrato/dados/YYYY-MM`)
- [ ] **AJAX endpoint works** - Returns JSON data
- [ ] **Data format correct** - Valid JSON structure
- [ ] **Month filtering works** - Only data for selected month

---

## 👥 Artists Management Tests

### Artists List (`/cadastro/artistas`)
- [ ] **Page loads correctly**
- [ ] **Artists display in table** - All artist data visible
- [ ] **Add new artist works** - Form submission successful
- [ ] **Edit artist works** - Modify existing artist
- [ ] **Delete artist works** - Remove artist (with confirmation)
- [ ] **Artist specialties display** - If applicable

### Artist Data Integrity
- [ ] **Commission rates saved** - Default commission percentages
- [ ] **Artist names consistent** - Same across all modules
- [ ] **Artist status works** - Active/inactive functionality

---

## 📦 Inventory Tests

### Inventory Management (`/estoque/`)
- [ ] **Page loads correctly**
- [ ] **Products display** - All inventory items visible
- [ ] **Add product works** - New product creation
- [ ] **Edit product works** - Modify existing product
- [ ] **Delete product works** - Remove product
- [ ] **Stock tracking works** - Quantity updates correctly

### Product Operations
- [ ] **Stock adjustments** - Increase/decrease stock
- [ ] **Product categories** - If applicable
- [ ] **Product search** - Find specific products

---

## 📋 History Module Tests

### History Overview (`/historico/`)
- [ ] **Page loads correctly**
- [ ] **All history sections visible** - Payments, Sessions, Commissions
- [ ] **Data displays correctly** - Historical data preserved
- [ ] **Navigation between sections** - Tabs or links work

### Payments History
- [ ] **Historical payments display** - All past payments
- [ ] **Data integrity maintained** - All payment details preserved
- [ ] **Edit historical payments** - Modify past payments
- [ ] **Delete historical payments** - Remove from history

### Sessions History
- [ ] **Historical sessions display** - All completed sessions
- [ ] **Commission data preserved** - Artist commissions shown
- [ ] **Edit historical sessions** - Modify past sessions
- [ ] **Delete historical sessions** - Remove from history

### Commissions History
- [ ] **Commission calculations** - Correct percentages and amounts
- [ ] **Artist commission totals** - Aggregate calculations
- [ ] **Edit commissions** - Modify commission entries
- [ ] **Delete commissions** - Remove commission entries

---

## 🧮 Calculator Tests

### Commission Calculator (`/calculadora/`)
- [ ] **Calculator loads correctly**
- [ ] **Input fields work** - Value and percentage inputs
- [ ] **Calculations accurate** - Commission amounts correct
- [ ] **Different percentages** - Test various commission rates
- [ ] **Edge cases handled** - Zero values, 100% commission

---

## 🔧 System Integration Tests

### Data Consistency
- [ ] **Artist names consistent** - Same across all modules
- [ ] **Date formats consistent** - DD/MM/YYYY format throughout
- [ ] **Currency formatting** - R$ XX.XX format consistent
- [ ] **Session-payment linking** - Payments correctly link to sessions

### Error Handling
- [ ] **Invalid form submissions** - Proper error messages
- [ ] **Missing required fields** - Form validation works
- [ ] **Invalid date formats** - Proper error handling
- [ ] **Database errors** - Graceful error handling

### Performance
- [ ] **Page load times** - Reasonable response times
- [ ] **Large data sets** - System handles multiple records
- [ ] **Concurrent users** - Multiple browser tabs work

---

## 📱 User Experience Tests

### Navigation
- [ ] **Menu navigation works** - All menu items accessible
- [ ] **Back button works** - Browser back button functions
- [ ] **Breadcrumb navigation** - If applicable
- [ ] **Mobile responsiveness** - Works on mobile devices

### Forms
- [ ] **Form auto-completion** - Browser auto-fill works
- [ ] **Tab navigation** - Tab key moves between fields
- [ ] **Enter key submission** - Forms submit with Enter
- [ ] **Form reset works** - Clear/reset buttons function

### Feedback
- [ ] **Success messages display** - Green success notifications
- [ ] **Error messages display** - Red error notifications
- [ ] **Loading indicators** - If applicable
- [ ] **Confirmation dialogs** - Delete confirmations work

---

## 🗄️ Data Backup Tests

### Backup Operations
- [ ] **Monthly backup works** - Backup process completes
- [ ] **Backup files created** - Files saved in correct location
- [ ] **Backup data integrity** - Backed up data is complete
- [ ] **Restore functionality** - If available

---

## 🔐 Security Tests

### Input Validation
- [ ] **SQL injection prevention** - System uses JSON files
- [ ] **XSS prevention** - User input properly escaped
- [ ] **CSRF protection** - Forms protected against CSRF
- [ ] **File upload security** - If applicable

---

## 📊 Final Validation

### System Status
- [ ] **No console errors** - Check browser developer tools
- [ ] **All features working** - Complete system functionality
- [ ] **Data persistence** - Data saved correctly between sessions
- [ ] **Session management** - User sessions work properly

### Business Logic
- [ ] **Commission calculations correct** - Artist commissions accurate
- [ ] **Total calculations correct** - All financial totals accurate
- [ ] **Date filtering works** - Monthly/yearly filtering functions
- [ ] **Search functionality** - Find specific records

---

## ✅ Testing Completion

### Final Checklist
- [ ] **All core features tested** - Sessions, Payments, Artists, Inventory
- [ ] **All forms tested** - Create, Edit, Delete operations
- [ ] **All reports tested** - Extracts, History, Totals
- [ ] **All integrations tested** - Module interactions work
- [ ] **Error scenarios tested** - System handles errors gracefully
- [ ] **Performance acceptable** - System responds quickly
- [ ] **User experience good** - Interface intuitive and functional

### Testing Summary
**Date Tested**: _______________  
**Tester Name**: _______________  
**Overall Status**: ⭐⭐⭐⭐⭐ (Rate 1-5 stars)  
**Critical Issues**: _______________  
**Recommendations**: _______________

---

## 📝 Notes

Use this space to document any issues found, suggestions for improvement, or additional test cases that should be added:

```
[Your testing notes here]
```

---

**Remember**: This checklist should be completed thoroughly before any production deployment. Each checkbox represents a critical functionality that users depend on.
