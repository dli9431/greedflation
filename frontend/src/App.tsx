import React, { useState, useEffect } from 'react';
import { createBrowserRouter, Outlet, RouterProvider } from "react-router-dom";

import {
  Fallback,
  Layout,
  RootErrorBoundary,
  ProjectErrorBoundary,
  projectLoader,
} from "./routes";

let router = createBrowserRouter([
  {
    path: "/",
    element: <Layout />,
    children: [
      {
        path: "",
        element: <Outlet />,
        errorElement: <RootErrorBoundary />,
        
        // children: [
        //   {
        //     path: "projects/:projectId",
        //     element: <Project />,
        //     errorElement: <ProjectErrorBoundary />,
        //     loader: projectLoader,
        //   },
        // ],
      },
    ],
  },
]);

export default function App() {
  return <RouterProvider router={router} fallbackElement={<Fallback />} />;
}