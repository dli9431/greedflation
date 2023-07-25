import { createBrowserRouter, RouterProvider, Outlet } from "react-router-dom";
import {
  Fallback,
  Layout,
  RootErrorBoundary,
  Project,
  ProjectErrorBoundary,
  projectLoader,
} from "./routes";
import { useState } from 'preact/hooks'
import './app.css'

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
            path: "projects/:projectId",
            element: <Project />,
            errorElement: <ProjectErrorBoundary />,
            loader: projectLoader,
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
