from reportlab.lib.pagesizes import letter
import textwrap
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
import streamlit as st



def wrap_text(text, max_width, c):
    wrapped_text = []
    for line in text.splitlines():
        wrapped_text.extend(textwrap.wrap(line, width=int(max_width / 6), expand_tabs=False))
    return wrapped_text

def format_directory(directory, indent=0):
    output = ""
    if isinstance(directory, dict):
        for item, value in directory.items():
            if value is None:
                output += ".   .    ." * indent + f"{item}\n"
            elif isinstance(value , str):
                output += f"{item}\n{value}"
            else:
                output += ".   .    ." * indent + f"{item}\n"
                output += format_directory(value, indent + 1)
    else:
        for i in directory:
            output+= format_directory(i, indent)
    return output

def format_directorySum(directory, indent=0):
    output = ""
    if isinstance(directory, dict):
        for item, value in directory.items():
            if isinstance(value , str):
                output += f"{item}\n{value}"
            else:
                output += format_directorySum(value, indent + 1)
    elif isinstance(directory, list):
        for i in directory:
            output+= format_directorySum(i, indent)
    return output


def genratePDF(pdf_filename, foldrstr,projSummary, longSummary):
    foldrstr_text = format_directory(foldrstr)
    longSummary_text = format_directorySum(longSummary)
    formatted_foldstr = foldrstr_text.split("\n")
    formatted_longSummary = longSummary_text.split("\n")
    doc = SimpleDocTemplate(f"{pdf_filename}.pdf", pagesize=letter)
    styles = {
        'default': ParagraphStyle(
            'default',
            fontName='Helvetica',
            fontSize=10,
            leading=12,
        ),
    'heading': ParagraphStyle(
        'heading',
        fontName='Helvetica-Bold',  # Using bold font for heading
        fontSize=14,  # Adjust as per your preference
        leading=16,  # Adjust leading for spacing if needed
        spaceAfter=12,  # Add space after the heading
    ),
    'subheading': ParagraphStyle(
        'heading',
        fontName='Helvetica-Bold',  # Using bold font for heading
        fontSize=12,  # Adjust as per your preference
        leading=16,  # Adjust leading for spacing if needed
        spaceAfter=12,  # Add space after the heading
    ),
    }
    content = []
    content.append(Paragraph("Project Title", styles["heading"]))
    content.append(Spacer(1,12))
    content.append(Paragraph("Summary", styles["subheading"]))
    content.append(Spacer(1,12))
    content.append(Paragraph(projSummary, styles["default"]))
    content.append(Spacer(1, 12))
    content.append(Paragraph("Folder Structure", styles["subheading"]))
    for line in formatted_foldstr:        
        content.append(Paragraph(line, styles['default']))
    content.append(Spacer(1, 24))
    content.append(Paragraph("Code Summaries", styles["subheading"]))
    for line in formatted_longSummary:        
        content.append(Paragraph(line, styles['default']))
        content.append(Spacer(1, 24))
    content.append(Spacer(1, 12))
    doc.build(content)
    # st.info("FILE CREATED!!!")
    

project_summary = """
Our project, "Smart Home Automation System," aims to revolutionize the way we interact with our living spaces by integrating cutting-edge IoT technology. The system enables users to control and monitor home appliances remotely via a mobile application, providing convenience, energy efficiency, and enhanced security. Key features include real-time energy consumption tracking, customizable automation schedules, and seamless integration with popular voice assistants.

Key Features:
- Remote control of home appliances through a mobile app
- Real-time energy consumption monitoring
- Customizable automation schedules for various devices
- Integration with voice assistants like Amazon Alexa and Google Assistant
- Enhanced security with real-time alerts and monitoring
"""

foldrstr = {
    "sign": {
        "project_Summary.pdf": None,
        "src": {
            "index.js": None,
            "index.css": None,
            "components": {
                "Navbar.js": None,
                "Carousel.js": None
            },
            "firebase": {
                "authsetup.js": None,
                "config.js": None
            },
            "pages": {
                "About.js": None,
                "Home.js": None,
                "Login.js": None,
                "Nopage.js": None,
                "Contact.js": None
            }
        }
    }
}

longSum = {
  "📁 :sign": [
    {
      "project_Summary.pdf": "Not a code file"
    },
    {
      "📁 :src": [
        {
          "index.js": "This code is a basic setup for a React application. It uses React and ReactDOM to render the main component 'App' onto the root element in the HTML document. The code also includes a call to reportWebVitals function for measuring performance in the application.\n\nTo summarize:\n- The code initializes a root element using ReactDOM.createRoot and renders the 'App' component inside a React.StrictMode wrapper.\n- It includes a call to reportWebVitals function for measuring performance in the application.\n- The index.css file is imported for styling purposes.\n\nThis code provides a simple starting point for a React project and can be expanded upon to build a more complex application."
        },
        {
          "index.css": "This code includes the Tailwind CSS base, components, and utilities. It also imports Google Fonts for the Cormorant Infant (300 weight) and Josefin Sans (200 and 400 weight) fonts.\n\nTo use this code in your project, make sure to have Tailwind CSS installed and configured. You can customize the fonts imported from Google Fonts by changing the URL or adding additional font families.\n\nRemember to include this code in your main CSS file or stylesheet to apply the Tailwind CSS styles and Google Fonts to your project."
        },
        {
          "📁 :components": [
            {
              "Navbar.js": "This code is a React component for a Navbar that includes a logo, navigation links, and a login button. Here is a brief documentation for this code:\n\n1. Import Statements:\n   - React is imported from the \"react\" library.\n   - Outlet and Link are imported from \"react-router-dom\".\n   - Login component is imported from \"../pages/Login\".\n   - Logo image is imported from '../assets/Logo.png'.\n\n2. Component Functionality:\n   - The Navbar component takes two props: getdets and userCred.\n   - It renders a navigation bar with a logo, navigation links, and a login button.\n   - If userCred is null, it displays a login button that triggers the getdets function.\n   - If userCred is not null, it displays the user's display name.\n   - The navigation links are rendered dynamically from the navitems array.\n\n3. HTML Structure:\n   - The Navbar component is wrapped inside a div with a custom brown background.\n   - It contains a navigation bar with a logo, navigation links, and a login button.\n   - The navigation links are displayed horizontally on larger screens and vertically on smaller screens.\n\n4. Styling:\n   - The component uses Tailwind CSS classes for styling, including custom colors, padding, and font styles.\n   - The logo is displayed with a specific size based on the screen size.\n   - The navigation links are styled with custom fonts and colors.\n\n5. Export:\n   - The Navbar component is exported as the default export from the file.\n\nOverall, this code provides a responsive Navbar component for a website with dynamic navigation links and a login button."
            },
            {
              "Carousel.js": "```jsx\n/*\n  Component: Carousel\n  Description: A carousel component that displays a series of images in a swiper carousel.\n*/\n\n// Import necessary libraries and modules\nimport React, { useEffect, useState } from 'react';\nimport { Swiper, SwiperSlide } from \"swiper/react\";\nimport \"swiper/css\";\nimport \"swiper/css/effect-coverflow\";\nimport 'swiper/css/pagination';\nimport { EffectCoverflow, Autoplay, Pagination } from \"swiper/modules\";\n\n// Import images for carousel\nimport img1 from \"../assets/carousel/Frame 3692.png\";\nimport img2 from \"../assets/carousel/Frame 3693.png\";\nimport img3 from \"../assets/carousel/Frame 3694.png\";\nimport img4 from \"../assets/carousel/Frame 3695.png\";\nimport img5 from \"../assets/carousel/Frame 3696.png\";\n\n// Define the Carousel component\nfunction Carousel({sPV}) {\n    // Array of image paths for the carousel\n    const imgs = [img1, img2, img3, img4, img5];\n\n    // Render the Swiper carousel component with specified settings\n    return (\n        <>\n            <Swiper\n                effect={\"coverflow\"}\n                grabCursor={true}\n                centeredSlides={true}\n                loop={true}\n                slidesPerView={sPV}\n                coverflowEffect={{\n                    rotate: 0,\n                    stretch: 0,\n                    depth: 100,\n                    modifier: 2.5,\n                    slideShadows: false\n                }}\n                autoHeight={false}\n                speed={2000}\n                autoplay={{ delay: 2500, disableOnInteraction: false }}\n                pagination={{ clickable: false }}\n                modules={[EffectCoverflow, Autoplay, Pagination]}\n                className={`lg: h-[400px] block rounded-t-[60px] rounded-b-[100px] md:h-[300px] sm:h-[250px]`}\n            >\n                {/* Map through the images array and render each image as a SwiperSlide */}\n                {imgs.map((img, index) => (\n                    <SwiperSlide key={index}>\n                        <div>\n                            <img src={img} className={`h-[350px] w-[800px] md:h-[280px] w-full sm:h-[240px] w-full`} />\n                        </div>\n                    </SwiperSlide>\n                ))}\n            </Swiper>\n        </>\n    )\n}\n\n// Export the Carousel component\nexport default Carousel;\n```"
            }
          ]
        },
        {
          "📁 :firebase": [
            {
              "authsetup.js": "The code snippet provided initializes Firebase Authentication UI and allows users to sign in using email or Google authentication methods. \n\nThe code first imports the necessary Firebase and FirebaseUI libraries. It then creates a new instance of the `AuthUI` class and starts the authentication UI on the specified HTML element with the `signInOptions` configuration, which includes email and Google authentication providers.\n\nIf there is a pending redirect for email link sign-in, the code checks for it and starts the authentication UI again. Alternatively, it also checks if the current URL is for email link sign-in and starts the authentication UI in that case.\n\nPlease note that this code snippet requires Firebase and FirebaseUI libraries to be properly set up and configured in your project. Additional configuration options can be added as needed for your specific project requirements."
            },
            {
              "config.js": "This code snippet is responsible for initializing Firebase in a web app and setting up authentication using Google provider.\n\n1. Import necessary functions from Firebase SDKs:\n- initializeApp from \"firebase/app\"\n- getAnalytics from \"firebase/analytics\"\n- getAuth, GoogleAuthProvider, signInWithPopup, setPersistence, signInWithRedirect, inMemoryPersistence from \"firebase/auth\"\n\n2. Define Firebase configuration with your project details like apiKey, authDomain, databaseURL, projectId, storageBucket, messagingSenderId, appId, and measurementId.\n\n3. Initialize Firebase with the provided configuration:\n- initializeApp(firebaseConfig)\n- getAnalytics(app)\n- getAuth(app)\n\n4. Optionally, you can set persistence for authentication using inMemoryPersistence and handle any errors that may occur during the process.\n\nMake sure to replace the placeholder values in firebaseConfig with your actual Firebase project details. This documentation provides an overview of the code's functionality and how it sets up Firebase authentication using Google provider in a web app."
            }
          ]
        },
        {
          "📁 :pages": [
            {
              "About.js": "### About Component Documentation\n\n#### Overview\nThe About component is responsible for displaying information about the company and its mission. It includes an image, text content, and animations that are triggered when the viewer scrolls to a certain point on the page.\n\n#### Dependencies\n- `react-animate-on-scroll`: This library is used for animating elements on scroll.\n- `react`: React library for building user interfaces.\n\n#### Props\nNone\n\n#### State\n- `writerimg`: Controls the visibility and styling of the writer image.\n- `pattern`: Controls the visibility and animation of a pattern image.\n- `aboutus`: Controls the styling of the text content.\n\n#### Functions\n- `handleScroll`: Listens for the scroll event and triggers animations when the viewer scrolls to a specific point on the page.\n\n#### Usage\nThe About component is used to display information about the company and create an engaging user experience on the website.\n\n#### Example\n```jsx\nimport img2 from \"../assets/about.jpeg\";\nimport ScrollAnimation from \"react-animate-on-scroll\";\nimport Pattern from \"../assets/Pattern.svg\";\nimport { useEffect, useLayoutEffect, useState } from \"react\";\n\nfunction About() {\n    // Component code goes here\n}\n\nexport default About;\n```"
            },
            {
              "Home.js": "### Project Documentation\n\n#### Code Description:\nThe `Home` component is responsible for rendering the home page of the application. It includes a background image, a headline, a subheading, and a button linking to the Instagram page of Signature Scribbles. It also includes sections for About, Benefits, and Contact components.\n\n#### Code Functionality:\n- Renders a background image with a headline and subheading.\n- Includes a button linking to the Instagram page of Signature Scribbles.\n- Displays sections for About, Benefits, and Contact components.\n\n#### Code Dependencies:\n- `img1.jpg` from \"../assets/img1.jpg\"\n- `About` component from \"./About\"\n- `Benefits` component from \"./Benefits\"\n- `Contact` component from \"./Contact\"\n\n#### Usage:\nThe `Home` component should be imported and rendered within the application to display the home page content.\n\n```javascript\nimport Home from \"./Home\";\n\nfunction App() {\n  return (\n    <div>\n      <Home />\n    </div>\n  );\n}\n\nexport default App;\n```\n\n#### Additional Notes:\n- The `Home` component requires the `userCred` prop to be passed to it.\n- Ensure that all dependencies are correctly imported and linked to the component."
            },
            {
              "Login.js": "The code provided is a React component for handling user authentication using Firebase Authentication. Here is a brief documentation for the code:\n\n1. The code imports necessary functions and components from Firebase Authentication SDK, Firebase UI, and Firebase configuration file.\n\n2. The `Login` component is a functional component that handles the UI for user authentication.\n\n3. The `useEffect` hook is used to initialize the Firebase UI authentication widget when the component is mounted.\n\n4. The `uiConfig` object contains configuration settings for the Firebase UI authentication widget, including callbacks for successful sign-in and UI customization.\n\n5. The `ui.start` method initializes the Firebase UI authentication widget with the specified configuration and mounts it to the `#firebaseui-auth-container` element.\n\n6. The component renders a heading, a container for the Firebase UI widget, and a loader element.\n\n7. The user can sign in using Google authentication by clicking on the Google sign-in button provided by the Firebase UI widget.\n\n8. Terms of service and privacy policy URLs are provided for users to read before signing in.\n\nOverall, the `Login` component provides a user-friendly interface for authentication using Firebase Authentication and Firebase UI."
            },
            {
              "Nopage.js": "/**\n * Component for displaying a page not found message.\n * \n * @component\n * @example\n * return (\n *   <Nopage />\n * )\n */\nimport React from 'react'\n\nfunction Nopage() {\n  return (\n    <div>Nopage</div>\n  )\n}\n\nexport default Nopage\n**/"
            },
            {
              "Contact.js": "This code defines a functional component called Contact, which displays a contact section on a web page. Here is a brief documentation for the code:\n\n1. Import: The code imports a logo image from the assets folder.\n\n2. Constants:\n   - contactButtons: An array containing the names of contact buttons (\"Home\", \"About\", \"Contact Us\").\n   - paths: An array containing SVG path data for social media icons.\n   - socials: An array containing URLs for social media profiles.\n\n3. Return:\n   - The component returns a div with the id \"Contact\" and a custom white background.\n   - It displays the imported logo image.\n   - It renders a list of contact buttons with links to corresponding sections on the page.\n   - It renders social media icons with links to respective social media profiles.\n   - It includes a copyright message at the bottom of the contact section.\n\n4. Export: The Contact component is exported as the default export from the file.\n\nOverall, the Contact component provides a visually appealing and functional contact section for a web page, including navigation links and social media icons."
            },
            {
              "Benefits.js": "This code is a React component called Benefits that renders a section on the benefits of journaling. The component includes a Carousel component that displays content in a carousel format based on screen size. \n\nThe useEffect hook is used to add an event listener to the window scroll event. When the user scrolls past 1000 pixels, the benefitsClass state is updated to include the \"animate-bottom-up\" class, triggering an animation to slide the content into view.\n\nThe rendered content includes a heading for the Benefits section and a heading for the benefits of journaling. The section is styled with a custom brown background color and includes responsive design for different screen sizes.\n\nOverall, this component is responsible for displaying information about the benefits of journaling in a visually appealing way."
            }
          ]
        },
        {
          "App.js": "This code is a React component that sets up routes for a web application using React Router. It includes imports for necessary components and pages, as well as authentication functionality using Firebase.\n\nThe `App` component sets up routes using `BrowserRouter` from React Router. It includes routes for the `Home` page, `Login` page, and a default `Nopage` component for routes that do not match any defined paths. The `Navbar` component is also included and passed the `getdets` function and `userCred` state as props.\n\nThe component uses `useState` to manage the `userCred` state, which stores the current user's authentication credentials. The `getdets` function is an asynchronous function that uses Firebase's `signInWithPopup` method with a GoogleAuthProvider to authenticate the user and set the `userCred` state with the user's data.\n\nOverall, this code sets up a basic routing structure for a web application with authentication functionality using Firebase."
        }
      ]
    }
  ]
}




genratePDF("Signature Scribbles",foldrstr,project_summary,longSum)