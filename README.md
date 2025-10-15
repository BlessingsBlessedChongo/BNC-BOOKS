# 📚 BNC Books - Modern Book Marketplace

![BNC Books](https://img.shields.io/badge/BNC-Books-brightgreen)
![Vue 3](https://img.shields.io/badge/Vue-3-4FC08D?logo=vue.js)
![Django](https://img.shields.io/badge/Django-REST-092E20?logo=django)
![Tailwind CSS](https://img.shields.io/badge/Tailwind-CSS-38B2AC?logo=tailwind-css)

A full-stack, modern book marketplace built with Vue.js and Django. BNC Books connects book lovers with sellers worldwide, offering a seamless shopping experience with advanced features for buyers, sellers, and affiliates.


https://github.com/user-attachments/assets/f50396af-22fe-40e8-ad28-fcdf8acf2e40
<img width="1919" height="878" alt="Screenshot 2025-10-15 014913" src="https://github.com/user-attachments/assets/b80cb36d-8a8d-4113-9c21-8cc6e3e251a8" />
<img width="1919" height="884" alt="Screenshot 2025-10-15 015014" src="https://github.com/user-attachments/assets/7f40a922-b01a-4f3e-a1a3-28ecaa92be8b" />
<img width="1914" height="875" alt="Screenshot 2025-10-15 015027" src="https://github.com/user-attachments/assets/f2ebcd51-50aa-444f-8639-5615e6142b80" />
<img width="1906" height="878" alt="Screenshot 2025-10-15 015038" src="https://github.com/user-attachments/assets/7ef6c306-90fd-407e-9863-1c1fc530d2b9" />
<img width="1919" height="878" alt="Screenshot 2025-10-15 015200" src="https://github.com/user-attachments/assets/144023ca-20d5-4841-9acd-19d428a75a09" />
<img width="1899" height="877" alt="Screenshot 2025-10-15 015217" src="https://github.com/user-attachments/assets/9e740478-5d23-4d79-bbbc-d714fe9eae88" />
<img width="1919" height="952" alt="Screenshot 2025-10-15 015343" src="https://github.com/user-attachments/assets/af689b69-d8e1-4dfe-8817-aeb2c72db8b3" />



## 🎯 Features

### 🛍️ For Book Buyers
- **Advanced Book Discovery** - Search, filter, and browse thousands of books
- **Smart Shopping Cart** - Persistent cart with real-time updates
- **Secure Checkout** - Multi-step checkout with multiple payment options
- **Order Tracking** - Real-time order status and tracking information
- **Review System** - Rate and review purchased books
- **Wishlist** - Save favorite books for later

### 🏪 For Sellers
- **Book Management** - Complete CRUD operations for book listings
- **Inventory Control** - Real-time stock management and adjustments
- **Order Fulfillment** - Process orders and update shipping status
- **Sales Analytics** - Comprehensive dashboard with revenue insights
- **Performance Metrics** - Track sales, views, and conversion rates

### 🤝 For Affiliates
- **Referral Program** - Generate custom referral links
- **Commission Tracking** - Real-time commission calculations
- **Performance Analytics** - Track clicks, conversions, and earnings
- **Payout System** - Request payments with multiple methods
- **Campaign Management** - Create and track marketing campaigns

## 🚀 Quick Start

### Prerequisites
- Node.js 16+
- Python 3.8+
- PostgreSQL/MySQL

### Frontend Setup

```bash
# Clone the repository
git clone https://github.com/your-username/bnc-books-frontend.git
cd bnc-books-frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

### Backend Setup

```bash
# Navigate to backend directory
cd bnc-books-backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Start development server
python manage.py runserver
```

The application will be available at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000

## 🛠️ Technology Stack

### Frontend
- **Vue 3** - Progressive JavaScript framework
- **Vite** - Next-generation build tool
- **Pinia** - State management
- **Vue Router** - Client-side routing
- **Tailwind CSS** - Utility-first CSS framework
- **Axios** - HTTP client for API calls
- **VueUse** - Collection of essential Vue composition utilities

### Backend
- **Django** - High-level Python web framework
- **Django REST Framework** - Powerful API toolkit
- **PostgreSQL** - Advanced open-source database
- **JWT Authentication** - Secure token-based auth
- **Celery** - Asynchronous task queue
- **Redis** - In-memory data structure store

## 📁 Project Structure

```
bnc-books-frontend/
├── src/
│   ├── components/     # Reusable Vue components
│   ├── views/          # Page-level components
│   ├── stores/         # Pinia state management
│   ├── router/         # Vue Router configuration
│   ├── utils/          # Helper functions and utilities
│   └── styles/         # Global styles and Tailwind
├── public/             # Static assets
└── package.json        # Dependencies and scripts

bnc-books-backend/
├── apps/
│   ├── accounts/       # User authentication & profiles
│   ├── books/          # Book catalog and management
│   ├── orders/         # Order processing
│   ├── reviews/        # Review system
│   └── affiliates/     # Affiliate program
├── config/             # Django settings
└── manage.py          # Django management script
```

## 🔧 Configuration

### Environment Variables

**Frontend (.env)**
```env
VITE_API_BASE_URL=http://localhost:8000/api
VITE_APP_NAME=BNC Books
VITE_APP_VERSION=1.0.0
```

**Backend (.env)**
```env
DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_URL=postgres://user:pass@localhost:5432/bnc_books
REDIS_URL=redis://localhost:6379
```

## 🎨 Key Features Deep Dive

### 🔍 Advanced Search & Filtering
- Full-text search across titles, authors, and descriptions
- Filter by category, price range, rating, and availability
- Sort by relevance, price, rating, and date
- Real-time search suggestions

### 🛒 Smart Shopping Experience
- Persistent cart across sessions
- Real-time stock validation
- Multiple shipping options
- Tax calculation based on location
- Secure payment processing

### 📊 Seller Analytics
- Revenue and sales tracking
- Inventory performance metrics
- Customer behavior insights
- Sales trend analysis
- Top-performing books

### 💰 Affiliate Program
- 10% commission on referred sales
- Custom referral links with campaign tracking
- Real-time commission dashboard
- Multiple payout methods (PayPal, Bank Transfer)
- Performance analytics and reporting

## 🚀 Deployment

### Frontend Deployment (Vercel/Netlify)
```bash
npm run build
# Deploy dist/ folder to your hosting service
```

### Backend Deployment (Heroku/DigitalOcean)
```bash
# Set up production environment variables
# Run migrations
python manage.py migrate
# Collect static files
python manage.py collectstatic
# Start production server
```

## 🧪 Testing

```bash
# Frontend tests
npm run test:unit
npm run test:e2e

# Backend tests
python manage.py test
```

## 📈 Performance

- **Lighthouse Score**: 95+ 
- **First Contentful Paint**: <1.5s
- **Largest Contentful Paint**: <2.5s
- **Time to Interactive**: <3s

## 🔒 Security Features

- JWT-based authentication with refresh tokens
- CSRF protection
- XSS prevention
- SQL injection protection
- Rate limiting on API endpoints
- Secure password hashing
- Input validation and sanitization

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🏆 Acknowledgments

- Vue.js team for the amazing framework
- Django REST Framework for robust API development
- Tailwind CSS for the utility-first CSS approach
- All our contributors and beta testers

## 📞 Support

- 📧 Email: support@bncbooks.com
- 🐛 [Issue Tracker](https://github.com/your-username/bnc-books/issues)
- 💬 [Discord Community](https://discord.gg/bnc-books)
- 📚 [Documentation](https://docs.bncbooks.com)

## 🌟 Show Your Support

If you find this project helpful, please give it a ⭐️ on GitHub!

---

**Built with ❤️ by the BNC Books Team**

*Transforming the way people discover and purchase books worldwide.*
