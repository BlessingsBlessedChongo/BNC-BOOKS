// SEO and meta tag utilities
import { ref, watch } from 'vue'
import { useRoute } from 'vue-router'

// Default meta tags
const defaultMeta = {
  title: 'BNC Books - Your Online Bookstore',
  description: 'Discover millions of books at BNC Books. Fiction, non-fiction, textbooks, and more with free shipping and great prices.',
  keywords: 'books, bookstore, online shopping, fiction, non-fiction, textbooks',
  image: '/images/bnc-books-og.jpg',
  type: 'website',
  siteName: 'BNC Books',
  twitterCard: 'summary_large_image'
}

// Current meta state
const currentMeta = ref({ ...defaultMeta })

// Update meta tags in the document head
export const updateMetaTags = (meta = {}) => {
  const mergedMeta = { ...defaultMeta, ...meta }
  currentMeta.value = mergedMeta

  // Update document title
  document.title = mergedMeta.title

  // Update meta tags
  updateMetaTag('description', mergedMeta.description)
  updateMetaTag('keywords', mergedMeta.keywords)
  
  // Open Graph tags
  updateMetaTag('og:title', mergedMeta.title, 'property')
  updateMetaTag('og:description', mergedMeta.description, 'property')
  updateMetaTag('og:image', mergedMeta.image, 'property')
  updateMetaTag('og:type', mergedMeta.type, 'property')
  updateMetaTag('og:site_name', mergedMeta.siteName, 'property')
  updateMetaTag('og:url', window.location.href, 'property')
  
  // Twitter Card tags
  updateMetaTag('twitter:card', mergedMeta.twitterCard)
  updateMetaTag('twitter:title', mergedMeta.title)
  updateMetaTag('twitter:description', mergedMeta.description)
  updateMetaTag('twitter:image', mergedMeta.image)
}

// Helper to update individual meta tags
const updateMetaTag = (name, content, attribute = 'name') => {
  let tag = document.querySelector(`meta[${attribute}="${name}"]`)
  
  if (!tag) {
    tag = document.createElement('meta')
    tag.setAttribute(attribute, name)
    document.head.appendChild(tag)
  }
  
  tag.setAttribute('content', content)
}

// Structured data (JSON-LD) for books
export const generateBookStructuredData = (book) => {
  return {
    '@context': 'https://schema.org',
    '@type': 'Book',
    name: book.title,
    author: {
      '@type': 'Person',
      name: book.author
    },
    isbn: book.isbn,
    publisher: book.publisher,
    datePublished: book.publication_date,
    description: book.description,
    bookFormat: 'https://schema.org/Paperback',
    inLanguage: book.language,
    numberOfPages: book.pages,
    aggregateRating: {
      '@type': 'AggregateRating',
      ratingValue: book.average_rating,
      ratingCount: book.review_count,
      bestRating: '5',
      worstRating: '1'
    },
    offers: {
      '@type': 'Offer',
      price: book.price,
      priceCurrency: 'USD',
      availability: book.stock_quantity > 0 ? 
        'https://schema.org/InStock' : 'https://schema.org/OutOfStock',
      seller: {
        '@type': 'Organization',
        name: book.seller?.store_name || 'BNC Books'
      }
    },
    image: book.cover_image
  }
}

// Structured data for reviews
export const generateReviewStructuredData = (review, book) => {
  return {
    '@context': 'https://schema.org',
    '@type': 'Review',
    author: {
      '@type': 'Person',
      name: `${review.user.first_name} ${review.user.last_name}`
    },
    datePublished: review.created_at,
    reviewRating: {
      '@type': 'Rating',
      ratingValue: review.rating,
      bestRating: '5',
      worstRating: '1'
    },
    name: review.title,
    reviewBody: review.comment,
    itemReviewed: {
      '@type': 'Book',
      name: book.title,
      author: {
        '@type': 'Person',
        name: book.author
      }
    }
  }
}

// Structured data for organization
export const generateOrganizationStructuredData = () => {
  return {
    '@context': 'https://schema.org',
    '@type': 'Organization',
    name: 'BNC Books',
    description: 'Your premier online bookstore with millions of titles',
    url: window.location.origin,
    logo: `${window.location.origin}/images/logo.png`,
    sameAs: [
      'https://www.facebook.com/bncbooks',
      'https://www.twitter.com/bncbooks',
      'https://www.instagram.com/bncbooks'
    ],
    contactPoint: {
      '@type': 'ContactPoint',
      telephone: '+1-555-0123',
      contactType: 'customer service',
      email: 'support@bncbooks.com',
      areaServed: 'US',
      availableLanguage: ['English', 'Spanish']
    }
  }
}

// Auto-update meta tags based on route
export const useRouteMeta = () => {
  const route = useRoute()
  
  watch(() => route, (newRoute) => {
    const meta = newRoute.meta || {}
    
    if (meta.title || meta.description) {
      updateMetaTags({
        title: meta.title ? `${meta.title} - BNC Books` : defaultMeta.title,
        description: meta.description || defaultMeta.description
      })
    }
  }, { immediate: true })
}

// Canonical URL management
export const setCanonicalUrl = (url = null) => {
  const canonicalUrl = url || window.location.href.split('?')[0] // Remove query params
  
  let link = document.querySelector('link[rel="canonical"]')
  if (!link) {
    link = document.createElement('link')
    link.rel = 'canonical'
    document.head.appendChild(link)
  }
  
  link.href = canonicalUrl
}

// Breadcrumb structured data
export const generateBreadcrumbStructuredData = (breadcrumbs) => {
  return {
    '@context': 'https://schema.org',
    '@type': 'BreadcrumbList',
    itemListElement: breadcrumbs.map((breadcrumb, index) => ({
      '@type': 'ListItem',
      position: index + 1,
      name: breadcrumb.name,
      item: breadcrumb.url
    }))
  }
}

// Sitemap generation helper (for dynamic routes)
export const generateSitemapUrls = (routes) => {
  const baseUrl = window.location.origin
  const urls = routes.map(route => ({
    loc: `${baseUrl}${route.path}`,
    lastmod: route.lastmod || new Date().toISOString().split('T')[0],
    changefreq: route.changefreq || 'weekly',
    priority: route.priority || '0.8'
  }))
  
  return urls
}

export default {
  updateMetaTags,
  generateBookStructuredData,
  generateReviewStructuredData,
  generateOrganizationStructuredData,
  useRouteMeta,
  setCanonicalUrl,
  generateBreadcrumbStructuredData,
  generateSitemapUrls
}