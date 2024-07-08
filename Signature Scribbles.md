## Signature Scribbles

The project is a web application developed using React for creating a platform called Signature Scribbles. The application includes features like journaling, user authentication using Firebase, and social media integration. The technologies used include React, Firebase (for authentication), and Tailwind CSS for styling. The project consists of various components such as Navbar, Carousel, Login, About, Home, Benefits, Contact, and Nopage. The functionalities of the application include displaying information about the company, showcasing benefits of journaling, providing contact details, and allowing users to log in using Google authentication. The application also includes a responsive design with animations for improved user experience.

          index.js
          index.css
               Navbar.js
               Carousel.js
               authsetup.js
               config.js
               About.js
               Home.js
               Login.js
               Nopage.js
               Contact.js


#project_Summary.pdf

Not a code file
#index.js

# Project Documentation

This project uses React to render the main application component `App` into the root element of the HTML document.

## Imports
```javascript
import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';
import reportWebVitals from './reportWebVitals';
```

- **React**: The core library for building user interfaces in React.
- **ReactDOM**: Provides DOM-specific methods that can be used at the top level of a web app.
- **'./index.css'**: Stylesheet for the project.
- **App**: The main application component.
- **reportWebVitals**: A function to measure the performance of the app.

## Functionalities
```javascript
const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
```

- Creates a root for rendering the React application.
- Renders the `App` component inside a `React.StrictMode` to highlight potential problems in the code.

```javascript
reportWebVitals();
```

- Calls the `reportWebVitals` function to measure the performance of the app.

## Additional Notes
- The `ReactDOM.createRoot` function is used to create a root for rendering React components. This is a new feature in React 18.
- The `React.StrictMode` component is used for highlighting potential problems in the code and deprecated features.
- The `reportWebVitals` function can be passed a function to log performance results or send them to an analytics endpoint.
#index.css

# Project Documentation

This project is a front-end web development project that utilizes Tailwind CSS for styling and incorporates Google Fonts for typography.

## Imports

```css
@tailwind base;
@tailwind components;
@tailwind utilities;

/* Fonts */
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Infant:wght@300&family=Josefin+Sans:wght@200;400&display=swap');
```

## Functionalities

### 1. Base styles
The `@tailwind base;` import brings in the base styles provided by Tailwind CSS, setting up the foundational styles for elements like headings, paragraphs, and lists.

### 2. Components
The `@tailwind components;` import includes pre-styled components like buttons, forms, and cards that can be easily used in the project.

### 3. Utilities
The `@tailwind utilities;` import provides utility classes for quick styling adjustments such as margin, padding, text alignment, and more.

### 4. Google Fonts
The `@import url('https://fonts.googleapis.com/css2?family=Cormorant+Infant:wght@300&family=Josefin+Sans:wght@200;400&display=swap');` import brings in the Cormorant Infant and Josefin Sans fonts from Google Fonts, providing additional typography options for the project.
#Navbar.js

# Project Documentation - Navbar Component

This documentation provides an overview of the Navbar component in the project. The Navbar component is responsible for rendering the navigation bar at the top of the application.

## Imports
```jsx
import React from "react";
import { Outlet } from "react-router-dom";
import Logo from '../assets/Logo.png';
```

## Functionalities
- **Navbar Component:** The Navbar component is a functional component that renders the navigation bar with links to different sections of the application.
- **navitems:** An array containing objects with the name and link of each navigation item.
- **Conditional Rendering:** Depending on whether the user is logged in or not, the Navbar component displays either a "Log in" button or the user's display name.

```jsx
function Navbar({ getdets, userCred }) {
  const navitems = [
    { name: "Home", link: "#Home" },
    { name: "About", link: "#About" },
    { name: "Benefits of Journalling", link: "#Benefits" },
    { name: "Contact", link: "#Contact" },
  ];

  return (
    <>
      <div className="bg-custom-brown">
        <nav className="bg-custom-brown scroll w-full z-20 top-0 start-0 border-b border-gray-200 md:pt-12 sm:pt-6">
          <div className="flex flex-wrap items-center justify-between mx-auto bg-custom-brown md:p-5  text-custom-white font-josefin items-center border-y-2 border-custom-white sm:p-2">
              <span className="self-center md:text-2xl font-semibold whitespace-nowrap dark:text-white sm:text-xl">
                <img className="md:w-[13.1875rem] md:h-[4rem] sm:w-[8rem] sm:h-[3rem]" src={Logo} alt="" />
              </span>
         
            {userCred == null ? (
              <div className="flex md:order-2 space-x-3 md:space-x-0 rtl:space-x-reverse"> 
                <button
                  onClick={getdets}
                  type="button"
                  className="text-white focus:ring-4  font-medium rounded-lg text-sm md:px-4 md:py-2 sm:px-2 sm:py-1 text-center"
                >
                  Log in
                </button>{" "}
              </div>
            ) : (
              <div className="flex md:order-2 space-x-3 md:space-x-0 rtl:space-x-reverse ">{userCred.user.displayName}</div>
            )}

            <div
              className="items-center justify-between hidden w-full md:flex md:w-auto md:order-1"
              id="navbar-sticky"
            >
              <ul className="flex flex-col p-4 md:p-0 mt-4 font-medium rounded-lg space-x-10 rtl:space-x-reverse md:flex-row md:mt-0  ">
                {navitems.map((item, index) => (
                  <li key={index}>
                    <a
                      href={item.link}
                      className="font-josefin font-thin block py-2 px-3 text-white text-[18px] rounded md:bg-transparent md:p-0"
                      aria-current="page"
                    >
                      {item.name}
                    </a>
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </nav>

        <Outlet />
      </div>
    </>
  );
}

export default Navbar;
```

This documentation provides a clear understanding of the Navbar component, its functionalities, and how it is implemented in the project.
#Carousel.js

# Project Documentation: Carousel Component

## Brief Explanation
This code snippet shows a React component called Carousel, which utilizes the Swiper library to create a carousel slider with coverflow effect and autoplay functionality.

## Imports
```javascript
import React, { useEffect, useState } from 'react';
import { Swiper, SwiperSlide } from "swiper/react";
import "swiper/css";
import "swiper/css/effect-coverflow";
import 'swiper/css/pagination';
import { EffectCoverflow, Autoplay, Pagination } from "swiper/modules";
import img1 from "../assets/carousel/Frame 3692.png";
import img2 from "../assets/carousel/Frame 3693.png";
import img3 from "../assets/carousel/Frame 3694.png";
import img4 from "../assets/carousel/Frame 3695.png";
import img5 from "../assets/carousel/Frame 3696.png";
```

## Functionalities
- `Carousel`: This function component takes a prop `sPV` (slidesPerView) and renders a Swiper carousel with coverflow effect and autoplay.
  ```javascript
  function Carousel({sPV}) {
      const imgs = [img1, img2, img3, img4, img5];

      return (
          <Swiper
              effect={"coverflow"}
              grabCursor={true}
              centeredSlides={true}
              loop={true}
              slidesPerView={sPV}
              coverflowEffect={{
                  rotate: 0,
                  stretch: 0,
                  depth: 100,
                  modifier: 2.5,
                  slideShadows: false
              }}
              autoHeight={false}
              speed={2000}
              autoplay={{ delay: 2500, disableOnInteraction: false }}
              pagination={{ clickable: false }}
              modules={[EffectCoverflow, Autoplay, Pagination]}
              className={`lg: h-[400px] block rounded-t-[60px] rounded-b-[100px] md:h-[300px] sm:h-[250px]`}
          >
              {imgs.map((img, index) => (
                  <SwiperSlide key={index}>
                      <div>
                          <img src={img} className={`h-[350px] w-[800px] md:h-[280px] w-full sm:h-[240px] w-full`} />
                      </div>
                  </SwiperSlide>
              ))}
          </Swiper>
      );
  }
  ```

## Explanation
- The `Carousel` component renders a Swiper carousel with coverflow effect using the Swiper library.
- It accepts a prop `sPV` which determines the number of slides visible at a time.
- The component maps through an array of image paths and renders them as slides within the carousel.
- Various Swiper configurations such as effect, autoplay, pagination, etc., are set within the Swiper component.

This documentation provides a clear overview of the Carousel component, its functionalities, and the necessary imports for the code snippet.
#authsetup.js

# Firebase Authentication UI Documentation

This documentation provides information on how to use Firebase Authentication UI in your project.

## Imports
```javascript
var firebase = require("firebase");
var firebaseui = require("firebaseui");
```

## Functionalities

### Initialize Firebase Authentication UI
```javascript
var ui = new firebaseui.auth.AuthUI(firebase.auth());
```

### Start Firebase Authentication UI with Sign-in Options
```javascript
ui.start("#firebaseui-auth-container", {
  signInOptions: [
    {
      provider: firebase.auth.EmailAuthProvider.PROVIDER_ID,
      signInMethod: firebase.auth.EmailAuthProvider.EMAIL_LINK_SIGN_IN_METHOD,
    },
    firebase.auth.GoogleAuthProvider.PROVIDER_ID,
  ],
  // Other config options...
});
```

### Check for Email Link Sign-in
```javascript
if (ui.isPendingRedirect()) {
  ui.start("#firebaseui-auth-container", uiConfig);
}
// This can also be done via:
if (firebase.auth().isSignInWithEmailLink(window.location.href)) {
  ui.start("#firebaseui-auth-container", uiConfig);
}
```

This documentation provides a brief explanation of the code, imports used, and the functionalities of the Firebase Authentication UI implementation in the project.
#config.js

# Project Documentation

This documentation provides an overview of the Firebase configuration and authentication setup in the project.

## Imports
```javascript
import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";
import { getAuth, GoogleAuthProvider, signInWithPopup, setPersistence, signInWithRedirect, inMemoryPersistence } from "firebase/auth";
```

## Firebase Configuration
```javascript
const firebaseConfig = {
  apiKey: "",
  authDomain: "signaturescribbles-e4059.firebaseapp.com",
  databaseURL: "https://signaturescribbles-e4059-default-rtdb.asia-southeast1.firebasedatabase.app",
  projectId: "signaturescribbles-e4059",
  storageBucket: "signaturescribbles-e4059.appspot.com",
  messagingSenderId: "864005954640",
  appId: "1:864005954640:web:674c9dd3ba6848af980555",
  measurementId: "G-KML261HL10"
};
```

## Functionality
- Initialize Firebase and get analytics
```javascript
export const app = initializeApp(firebaseConfig);
export const analytics = getAnalytics(app);
```

- Get authentication instance and set persistence
```javascript
export const auth = getAuth(app)
// setPersistence(auth, inMemoryPersistence)
//   .then(() => {
//     const provider = new GoogleAuthProvider();
//     // In memory persistence will be applied to the signed in Google user
//     // even though the persistence was set to 'none' and a page redirect
//     // occurred.
//     return signInWithRedirect(auth, provider);
//   })
//   .catch((error) => {
//     // Handle Errors here.
//     const errorCode = error.code;
//     const errorMessage = error.message;
//   });
```

This code initializes Firebase with the provided configuration, sets up analytics, and handles authentication using Google provider with in-memory persistence.
#About.js

# About Component Documentation

## Brief Explanation
The About component is a React functional component that displays information about a particular entity or organization. It includes an animation that triggers when the viewer scrolls to a specific location on the page.

## Imports
```javascript
import img2 from "../assets/about.jpeg";
import ScrollAnimation from "react-animate-on-scroll";
import Pattern from "../assets/Pattern.svg";
import { useEffect, useLayoutEffect, useState } from "react";
```

## Functionalities
- The component includes state variables `writerimg`, `pattern`, and `aboutus` using the `useState` hook to manage the animation and content display.
- The `useEffect` hook is used to add an event listener to the window scroll event and trigger the animation when the viewer scrolls to a specific position on the page.
- The `handleScroll` function changes the state variables based on the scroll position to reveal the animation.
- The component renders HTML elements with dynamic classes based on the state variables to achieve the desired animation effect.

```javascript
function About() {
    const [writerimg, setWriterimg] = useState("hidden rounded-tr-[15rem] w-[34.6875rem] h-[42.53156rem] ml-10");
    const [pattern, setPattern] = useState("hidden");
    const [aboutus, setAboutus] = useState("p-10 ml-20 mb-40 lg:w-1/2");

    useEffect(() => {
        const handleScroll = () => {
            if(window.scrollY > 350){
                setPattern("animate-side-ways-spin");
                setWriterimg("animate-side-ways rounded-tr-[15rem] w-[34.6875rem] h-[42.53156rem] ml-10");
                setAboutus("animate-bottom-up p-10 ml-20 mb-40 lg:w-1/2");
            }
        };

        window.addEventListener('scroll', handleScroll);
        return () => window.removeEventListener('scroll', handleScroll);
    }, []);

    return (
        <div className="bg-custom-white flex" id="About">
            <div className="pattern absolute z-0 left-1/3 mt-36 hidden lg:block opacity-25 transition ">
                <img src={Pattern} alt="" className={pattern}/>
            </div>

            <div className="w-1/2 p-10 mt-20 z-10 hidden lg:block lg:w-1/2">
                <img
                    className={writerimg}
                    src={img2}
                    alt=""
                />
            </div>

            <div className={aboutus}>
                <div className="font-josefin mt-20 pb-5 pt-20">
                    <h2 className="border-t border-b border-solid p-1 border-custom-yellow font-josefin leading-[77.1%] tracking-[0.25313rem] inline">
                        ABOUT US
                    </h2>
                </div>
                <h1 className="text-4xl font-cormorant font-black pb-5 text-[2.5rem] text-custom-light-text">
                    Where Pages Pulse with Possibility.
                </h1>
                <p className=" font-josefin leading-8 text-[1.25rem] leading-7 text-custom-lighter-text">
                    We're not just journal sellers; we're architects of imagination. Our journey began with the belief that pen and paper wield transformative power. Crafting elegance, we champion individuality. Your unique story finds its canvas here. With unwavering commitment, we invite you to explore, create, and turn moments into memories. Welcome to creativity's sanctuary. Welcome to Signature Scribbles.
                </p>
            </div>
        </div>
    );
}

export default About;
```
#Home.js

# Project Documentation

## Home Component

The `Home` component is a functional component that renders the homepage of the application. It displays a brief introduction to the product and provides buttons to explore more information. It also includes components for 'About', 'Benefits', and 'Contact' sections.

### Imports:
```javascript
import img1 from "../assets/img1.jpg";
import About from "./About";
import Benefits from "./Benefits";
import Contact from "./Contact";
```

- `img1`: Importing the image file `img1.jpg` from the assets folder.
- `About`: Importing the About component to display information about the product.
- `Benefits`: Importing the Benefits component to showcase the benefits of the product.
- `Contact`: Importing the Contact component to provide contact information.

### Functionalities:
```javascript
function Home({ userCred }) {
  return (
    <>
      // Home section with product introduction and button
      <div className="flex bg-custom-brown md:h-[45rem] sm:h-[30rem]" id="Home">
        // Left section with product introduction
        <div className="md:p-10 sm:p-2 md:w-1/2 sm:w-2/3 md:h-full md:mt-20 sm:mt-10">
          // Product introduction text
          <div className="text-custom-white md:text-center md:mt-10">
            <p className="font-cormorant font-thin  leading-tight animate-bottom-up-fast md:p-5  md:text-5xl sm:text-2xl sm:p-1">
              Ink Your Identity, Bind Your Thoughts, Elevate Your Journaling
              with Signature Scribbles
            </p>
            <p className="font-josefin md:text-3xl sm:text-l md:mb-10 sm:mb-2 font-thin">
              Elevating Expression, One Page at a Time.
            </p>
          </div>
          // Button to explore more
          <div className="flex md:justify-center lg:justify-start sm:justify-start">
            <button className="border border-solid border-custom-yellow text-custom-white md:mx-10 md:py-5 md:px-10 sm:py-2 sm:px-3 text-2xl font-josefin">
              <a
                href="https://www.instagram.com/signature.scribbles/"
                target="_blank"
              >
                Know more
              </a>
            </button>
          </div>
        </div>
        
        // Right section with image
        <div className="mt-4 lg:mr-20 sm:mr-2 p-0 md:w-1/2 sm:w-1/3">
          // Image section
          <div className="rounded-t-[50rem] bg-custom-white px-10 pt-10 bg-opacity-5 backdrop-blur-[25.5px] h-[47rem]">
            <img
              className="animate-bottom-up rounded-t-[50rem] z-1 relative box-shadow-2xl md:h-[47rem]"
              src={img1}
              alt=""
            />
          </div>
        </div>
      </div>
      
      // Display About section
      <About />
      
      // Display Benefits section
      <Benefits />
      
      // Display Contact section
      <Contact />
    </>
  );
}

export default Home;
```

The `Home` component renders the homepage with a product introduction, button to explore more, and sections for 'About', 'Benefits', and 'Contact'. The component imports necessary assets and components to display the content effectively.
#Login.js

# Login Component Documentation

This component is responsible for rendering the login interface using Firebase authentication. It utilizes the Firebase Auth SDK and FirebaseUI for authentication purposes.

## Imports
```javascript
import { useEffect } from "react";
import { getAuth, onAuthStateChanged } from "firebase/auth";
import firebase from "firebase/compat/app";
import * as firebaseui from "firebaseui";
import "firebaseui/dist/firebaseui.css";
import { app, auth } from "../firebase/config";
import { GoogleAuthProvider } from "firebase/auth";
```

## Functionalities
1. **Initialization of FirebaseUI AuthUI Instance**
```javascript
const ui = firebaseui.auth.AuthUI.getInstance() || new firebaseui.auth.AuthUI(auth);
```
This code snippet initializes the FirebaseUI AuthUI instance using the existing instance or creates a new one using the `auth` object.

2. **Effect Hook for Firebase Authentication**
```javascript
useEffect(() => {
    // Configuration object for FirebaseUI
    var uiConfig = {
        callbacks: {
            signInSuccessWithAuthResult: function(authResult, redirectUrl) {
                // User successfully signed in
                // Return type determines further actions
                return true;
            },
            uiShown: function() {
                // Hide the loader once the UI is rendered
                document.getElementById('loader').style.display = 'none';
            }
        },
        signInFlow: 'popup',
        signInSuccessUrl: '/',
        signInOptions: [
            {
                provider: firebase.auth.GoogleAuthProvider.PROVIDER_ID,
                clientID: "YOUR_GOOGLE_CLIENT_ID"
            }
        ],
        tosUrl: '/terms',
        privacyPolicyUrl: '/privacy'
    };
    // Start the FirebaseUI with the specified configuration
    ui.start("#firebaseui-auth-container", uiConfig);
}, []);
```
This code snippet sets up the FirebaseUI configuration and initializes the FirebaseUI instance with the specified configuration when the component mounts.

3. **Login Interface Rendering**
```javascript
return (
    <>
      <h4>Signature Scribbles Login</h4>
      <div id="firebaseui-auth-container"></div>
      <div id="loader">Loading...</div>
    </>
);
```
This code snippet renders the login interface with the specified title and UI elements.

This documentation provides an overview of the Login component, including its imports and functionalities for handling Firebase authentication.
#Nopage.js

# Project Documentation

This project documentation provides an overview of the code and functionality of the Nopage component.

## Nopage Component

The Nopage component is a functional component in React that simply displays the text "Nopage".

### Imports
```javascript
import React from 'react'
```

The code snippet above imports the React library which is necessary for building React components.

### Functionality
```javascript
function Nopage() {
  return (
    <div>Nopage</div>
  )
}
```

The `Nopage` function is a functional component that returns a JSX element with the text "Nopage". This component can be used to display a message when a page is not found.

```javascript
export default Nopage
```

The `export default Nopage` statement exports the Nopage component so that it can be imported and used in other parts of the application.

This documentation provides a brief explanation of the Nopage component, its imports, and functionality in Markdown format as per the guidelines.
#Contact.js

# Project Documentation

This document provides an overview of the Contact component in the project. The Contact component displays various contact buttons and social media links for the Signature Scribbles website.

## Imports
```javascript
import logo from "../assets/contact_logo.png";
```

## Functionality
- **contactButtons**: An array containing the names of contact buttons ("Home", "About", "Contact Us").
- **paths**: An array of SVG path data for social media icons.
- **socials**: An array of social media URLs.

```javascript
function Contact() {
  const contactButtons = ["Home", "About", "Contact Us"];

  const paths = [
    // SVG path data for different social media icons
  ];

  const socials = [
    "https://www.facebook.com/signature.scribbles/",
    "https://www.instagram.com/signature.scribbles/",
    "https://www.threads.net/@signature.scribbles"
  ]; 

  return (
    // JSX code to display contact buttons, social media icons, and copyright information
  );
}
```

The `Contact` component renders a section with contact buttons, social media icons, and copyright information for the Signature Scribbles website. The component uses the imported logo for display.

- The contact buttons are displayed as links in a horizontal row.
- Social media icons are displayed as SVG images with links to respective social media profiles.
- Copyright information is displayed at the bottom of the section.

By following the guidelines and including the relevant information in the documentation, users can easily understand the purpose and functionality of the Contact component in the project.
#Benefits.js

# Benefits Component Documentation

This document provides an overview of the Benefits component in the project. The Benefits component is responsible for displaying the benefits of journaling and includes a carousel for displaying information.

## Imports
```javascript
import Carousel from "../components/Carousel";
import { useEffect, useState } from "react";
```
- **Carousel**: This import is used to include the Carousel component in the Benefits component.
- **useEffect, useState**: These imports are used from React to manage component side effects and state respectively.

## Functionalities
- The Benefits component includes a state variable `benefitsClass` which is used to control the CSS classes applied to certain elements based on scroll position.
- The `useEffect` hook is used to add an event listener to the window scroll event. When the window scroll position exceeds 1000 pixels, the `benefitsClass` state is updated to trigger an animation effect.
- The component returns a JSX structure that displays the benefits section with a title and carousel component based on screen size.

```javascript
function Benefits() {
      const [benefitsClass, setBenefitsClass]= useState("hidden flex flex-col justify-center ")
      useEffect(() => {
          const handleScroll = () => {
            if(window.scrollY > 1000){
              setBenefitsClass("animate-bottom-up flex flex-col justify-center ")
            }
  
          };
          window.addEventListener('scroll', handleScroll);
          return () => window.removeEventListener('scroll', handleScroll);
        }, []);
      
  return (
    <div className=" bg-custom-brown p-28" id="Benefits">
      <div className={benefitsClass}>
        <h1 className="text-center relative p-1 font-josefin text-[1rem] tracking-[0.5rem] mb-6">
          <span className="border-t border-b p-2 border-solid border-y-custom-yellow text-custom-white">
            BENEFITS
          </span>
        </h1>
        <h1 className="text-center font-cormorant font-bold md:text-[2.65rem] text-custom-white leading-[2.61688rem] mb-9 sm:text-[2rem]">
          Benefits of Journaling
        </h1>
      </div>
      <div className="lg:block md:hidden sm:hidden hidden">
        <Carousel sPV={2}/>
      </div>
      <div className="lg:hidden md:block sm:block">
        <Carousel sPV={1}/>
      </div>
    </div>
  );
}

export default Benefits;
```

This Markdown document provides a structured overview of the Benefits component in the project, explaining its imports and functionalities.
#App.js

# Project Documentation

## App Component

### Imports:
```javascript
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Home from "./pages/Home";
import Navbar from "./components/Navbar";
import Nopage from "./pages/Nopage";
import Login from "./pages/Login";
import { auth } from "./firebase/config.js";
import { GoogleAuthProvider, signInWithPopup } from "firebase/auth";
import React, { useState } from "react";
```

### Functionality:
- The `App` component is the main component of the project.
- It utilizes React Router for navigation and authentication with Firebase.
- It includes the `Navbar`, `Home`, `Login`, and `Nopage` components.
- It uses Firebase's authentication methods to handle user credentials.

### Code Snippets:
```javascript
const [userCred, setUserCred] = useState(auth.currentUser);

const getdets = async () => {
  const userData = await signInWithPopup(auth, new GoogleAuthProvider());
  setUserCred(userData);
  console.log(userCred);
};

<BrowserRouter>
  <Routes>
    <Route element={<Navbar getdets={getdets} userCred={userCred} />}>
      <Route index element={<Home userCred={userCred} />} />
      <Route element={<Login />} path="/login" />
      <Route element={<Nopage />} path="*" />
    </Route>
  </Routes>
</BrowserRouter>
```

### Explanation:
- The `App` component uses React's `useState` hook to manage the current user's credentials.
- The `getdets` function is an asynchronous function that uses Firebase's `signInWithPopup` method to authenticate the user with Google.
- The component structure includes a `BrowserRouter` with nested `Routes` and `Route` components for navigation.
- The `Navbar` component is passed the `getdets` function and `userCred` state as props.
- The `Home`, `Login`, and `Nopage` components are rendered based on the route configuration.
