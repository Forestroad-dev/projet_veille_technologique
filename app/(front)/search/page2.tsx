import ProductItem from '@/components/products/ProductItem'
import { Rating } from '@/components/products/Rating'
import productServices from '@/lib/services/productService'
import Link from 'next/link'
import recommendedProducts from '@/app/api/recommendation'
import React, { useState, useEffect } from 'react';
import { Product } from '@/lib/models/ProductModel'
import { useClient } from 'next/client';
const sortOrders = ['newest', 'lowest', 'highest', 'rating']
const prices = [
  {
    name: '$1 to $50',
    value: '1-50',
  },
  {
    name: '$51 to $200',
    value: '51-200',
  },
  {
    name: '$201 to $1000',
    value: '201-1000',
  },
]

const ratings = [5, 4, 3, 2, 1]

export async function generateMetadata({
  searchParams: { q = 'all', category = 'all', price = 'all', rating = 'all' },
}: {
  searchParams: {
    q: string
    category: string
    price: string
    rating: string
    sort: string
    page: string
  }
}) {
  if (
    (q !== 'all' && q !== '') ||
    category !== 'all' ||
    rating !== 'all' ||
    price !== 'all'
  ) {
    return {
      title: `Search ${q !== 'all' ? q : ''}
          ${category !== 'all' ? ` : Category ${category}` : ''}
          ${price !== 'all' ? ` : Price ${price}` : ''}
          ${rating !== 'all' ? ` : Rating ${rating}` : ''}`,
    }
  } else {
    return {
      title: 'Search Products',
    }
  }
}

export default async function SearchPage({
  searchParams: {
    q = 'all',
    category = 'all',
    price = 'all',
    rating = 'all',
    sort = 'newest',
    page = '1',
  },
}: {
  searchParams: {
    q: string
    category: string
    price: string
    rating: string
    sort: string
    page: string
  }
}) {
  const [recommendedProducts, setRecommendedProducts] = useState<Product[]>([]);

  useEffect(() => {
    // Appel du gestionnaire (handler) avec le terme de recherche
    const fetchRecommendedProducts = async () => {
      try {
        const response = await fetch(`/api/recommendation?search=${encodeURIComponent(q)}`);
        if (!response.ok) {
          throw new Error('Failed to fetch recommended products');
        }
        const { products } = await response.json();
        setRecommendedProducts(products);
      } catch (error) {
        console.error('Error fetching recommended products:', error);
      }
    };

    fetchRecommendedProducts();
  }, [q]);
  const getFilterUrl = ({
    c,
    s,
    p,
    r,
    pg,
  }: {
    c?: string
    s?: string
    p?: string
    r?: string
    pg?: string
  }) => {
    const params = { q, category, price, rating, sort, page }
    if (c) params.category = c
    if (p) params.price = p
    if (r) params.rating = r
    if (pg) params.page = pg
    if (s) params.sort = s
    return `/search?${new URLSearchParams(params).toString()}`
  }
  const categories = await productServices.getCategories()
  const { countProducts, products, pages } = await productServices.getByQuery({
    category,
    q,
    price,
    rating,
    page,
    sort,
  })
  return (
    <div className="grid md:grid-cols-5 md:gap-5">
      {/* Sidebar pour les filtres de recherche */}
      <div>
        <div className="text-xl pt-3">Department</div>
        <div>
          <ul>
            {/* Filtrer par catégorie */}
            <li>
              <Link
                className={`link link-hover ${
                  'all' === category && 'link-primary'
                }`}
                href={getFilterUrl({ c: 'all' })}
              >
                Any
              </Link>
            </li>
            {categories.map((c: string) => (
              <li key={c}>
                <Link
                  className={`link link-hover ${
                    c === category && 'link-primary'
                  }`}
                  href={getFilterUrl({ c })}
                >
                  {c}
                </Link>
              </li>
            ))}
          </ul>
        </div>
        <div>
          <div className="text-xl pt-3">Price</div>
          <ul>
            {/* Filtrer par prix */}
            <li>
              <Link
                className={`link link-hover ${
                  'all' === price && 'link-primary'
                }`}
                href={getFilterUrl({ p: 'all' })}
              >
                Any
              </Link>
            </li>
            {prices.map((p) => (
              <li key={p.value}>
                <Link
                  href={getFilterUrl({ p: p.value })}
                  className={`link link-hover ${
                    p.value === price && 'link-primary'
                  }`}
                >
                  {p.name}
                </Link>
              </li>
            ))}
          </ul>
        </div>
        <div>
          <div className="text-xl pt-3">Customer Review</div>
          <ul>
            {/* Filtrer par évaluation du client */}
            <li>
              <Link
                href={getFilterUrl({ r: 'all' })}
                className={`link link-hover ${
                  'all' === rating && 'link-primary'
                }`}
              >
                Any
              </Link>
            </li>
            {ratings.map((r) => (
              <li key={r}>
                <Link
                  href={getFilterUrl({ r: `${r}` })}
                  className={`link link-hover ${
                    `${r}` === rating && 'link-primary'
                  }`}
                >
                  <Rating caption={' & up'} value={r}></Rating>
                </Link>
              </li>
            ))}
          </ul>
        </div>
      </div>
      {/* Contenu principal */}
      <div className="md:col-span-4">
        {/* Barre de recherche et options de tri */}
        <div className="flex items-center justify-between  py-4">
          <div className="flex items-center">
            {/* Affichage du nombre de résultats et des filtres sélectionnés */}
            {products.length === 0 ? 'No' : countProducts} Results
            {q !== 'all' && q !== '' && ' : ' + q}
            {category !== 'all' && ' : ' + category}
            {price !== 'all' && ' : Price ' + price}
            {rating !== 'all' && ' : Rating ' + rating + ' & up'}
            &nbsp;
            {/* Bouton pour effacer les filtres */}
            {(q !== 'all' && q !== '') ||
            category !== 'all' ||
            rating !== 'all' ||
            price !== 'all' ? (
              <Link className="btn btn-sm btn-ghost" href="/search">
                Clear
              </Link>
            ) : null}
          </div>
          {/* Options de tri */}
          <div>
            Sort by{' '}
            {sortOrders.map((s) => (
              <Link
                key={s}
                className={`mx-2 link link-hover ${
                  sort == s ? 'link-primary' : ''
                } `}
                href={getFilterUrl({ s })}
              >
                {s}
              </Link>
            ))}
          </div>
        </div>
        {/* Affichage des produits de recherche */}
        <div className="grid grid-cols-1 gap-4 md:grid-cols-3">
          {products.map((product) => (
            <ProductItem key={product.slug} product={product} />
          ))}
        </div>
        {/* Pagination */}
        <div className="join">
          {products.length > 0 &&
            Array.from(Array(pages).keys()).map((p) => (
              <Link
                key={p}
                className={`join-item btn ${
                  Number(page) === p + 1 ? 'btn-active' : ''
                } `}
                href={getFilterUrl({ pg: `${p + 1}` })}
              >
                {p + 1}
              </Link>
            ))}
        </div>
          {/* Afficher les produits recommandés */}
        <div className="grid grid-cols-1 gap-4 md:grid-cols-3">
          {recommendedProducts.map((product) => (
            <ProductItem key={product.slug} product={product} />
          ))}
        </div>   
        {/* Pagination */}
        <div className="join">
          {products.length > 0 &&
            Array.from(Array(pages).keys()).map((p) => (
              <Link
                key={p}
                className={`join-item btn ${
                  Number(page) === p + 1 ? 'btn-active' : ''
                } `}
                href={getFilterUrl({ pg: `${p + 1}` })}
              >
                {p + 1}
              </Link>
            ))}
        </div>
      </div>
    </div>
  )
  
}
