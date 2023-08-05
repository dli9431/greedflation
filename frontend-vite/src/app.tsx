import { useState } from 'react'
import reactLogo from './assets/react.svg'
import { json, createBrowserRouter, RouterProvider, Outlet } from "react-router-dom";
import {
  Fallback,
  Layout,
  RootErrorBoundary,
  ProductView,
  ProductErrorBoundary,
  productLoader,
} from "./routes";
import { Product } from './types/types';

let router = createBrowserRouter([
  {
    path: "/",
    element: <Layout />,
    children: [
      {
        path: "",
        element: <Outlet />,
        errorElement: <RootErrorBoundary />,
        children: [
          {
            path: 'store/:storename/product/:productId',
            // path: "?store=:storename&product=:productid",
            element: <ProductView />,
            errorElement: <ProductErrorBoundary />,
            // loader: productLoader,
            loader: async ({ params }) => {
              const productResponse = await fetch(`http://localhost:5000/api/store/${params.storename}/product/${params.productId}`, {
                method: 'GET',
              });
              const product: Product = await productResponse.json();
              console.log(product[0])
              return json(product[0]);

              // const product: Product = await fetch(`http://localhost:5000/api/store/${params.storename}/product/${params.productId}`, {
              //   method: 'GET',
              // }).then((res) => console.log(res));
              // console.log(product);

              // return json(product);
            },
          },
        ],
      },
    ],
  },
]);

export default function App() {
  return (
    <>
      <RouterProvider router={router} fallbackElement={<Fallback />} />
    </>
  )
}
