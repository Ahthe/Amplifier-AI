# 1. SignUp and SignIn Flow:

# Detailed SignUp and SignIn Flow with Directory Structure

## Directory Structure:
/src
|-- /actions
|   `-- /auth
|       `-- index.ts (onCompleteUserRegistration)
|-- /app
|   `-- /auth
|       |-- /sign-in
|       |   `-- page.tsx (SignInPage)
|       `-- /sign-up
|           `-- page.tsx (SignUp)
|-- /components
|   |-- /forms
|   |   |-- /sign-in
|   |   |   |-- form-provider.tsx (SignInFormProvider)
|   |   |   `-- login-form.tsx (LoginForm)
|   |   `-- /sign-up
|   |       |-- button-handlers.tsx (ButtonHandler)
|   |       |-- form-provider.tsx (SignUpFormProvider)
|   |       |-- highlight-bar.tsx (HighLightBar)
|   |       `-- registration-step.tsx (RegistrationFormStep)
|   `-- /ui
|       |-- button.tsx
|       `-- use-toast.ts
|-- /context
|   `-- use-auth-context.ts (useAuthContextHook)
|-- /hooks
|   |-- /sign-in
|   |   `-- use-sign-in.ts (useSignInForm)
|   `-- /sign-up
|       `-- use-sign-up.ts (useSignUpForm)
|-- /lib
|   `-- prisma.ts (Prisma client)
`-- /schemas
    `-- auth.schema.ts (UserRegistrationSchema, UserLoginSchema)

## Detailed Flow Diagram:

Sign-Up Flow:
+----------------------------------------------+
|                   SignUp                     |
| (/src/app/auth/sign-up/page.tsx)             |
|  +---------------------------------------+   |
|  |           SignUpFormProvider          |   |
|  | (/src/components/forms/sign-up/       |   |
|  |  form-provider.tsx)                   |   |
|  |  +------------------------------------+   |
|  |  |        RegistrationFormStep        |   |
|  |  | (/src/components/forms/sign-up/    |   |
|  |  |  registration-step.tsx)            |   |
|  |  |  - Manages multiple form steps     |   |
|  |  |  - Uses useFormContext             |   |
|  |  +------------------------------------+   |
|  |  +------------------------------------+   |
|  |  |           ButtonHandler            |   |
|  |  | (/src/components/forms/sign-up/    |   |
|  |  |  button-handlers.tsx)              |   |
|  |  | - Handles form submission          |   |
|  |  | - Manages OTP generation           |   |
|  |  +------------------------------------+   |
|  |  +------------------------------------+   |
|  |  |           HighLightBar             |   |
|  |  | (/src/components/forms/sign-up/    |   |
|  |  |  highlight-bar.tsx)                |   |
|  |  | - Visual feedback for form steps   |   |
|  |  +------------------------------------+   |
|  +----------------------------------------+  |
+----------------------------------------------+
                      |
                      | useSignUpForm hook
                      | (/src/hooks/sign-up/use-sign-up.ts)
                      v
+----------------------------------------------+
|           Clerk Authentication               |
| - signUp.create                              |
| - signUp.prepareEmailAddressVerification     |
| - signUp.attemptEmailAddressVerification     |
+----------------------------------------------+
                      |
                      v
+----------------------------------------------+
|          Database (via Prisma)               |
| (/src/lib/prisma.ts)                         |
| - onCompleteUserRegistration                 |
|   (/src/actions/auth/index.ts)               |
+----------------------------------------------+

Sign-In Flow:
+----------------------------------------------+
|                 SignInPage                   |
| (/src/app/auth/sign-in/page.tsx)             |
|  +----------------------------------------+  |
|  |          SignInFormProvider            |  |
|  | (/src/components/forms/sign-in/        |  |
|  |  form-provider.tsx)                    |  |
|  |  +------------------------------------+  |
|  |  |            LoginForm               |  |
|  |  | (/src/components/forms/sign-in/    |  |
|  |  |  login-form.tsx)                   |  |
|  |  | - Email and password inputs        |  |
|  |  | - Form submission handling         |  |
|  |  +------------------------------------+  |
|  +----------------------------------------+  |
+----------------------------------------------+
                      |
                      | useSignInForm hook
                      | (/src/hooks/sign-in/use-sign-in.ts)
                      v
+----------------------------------------------+
|           Clerk Authentication               |
| - signIn.create                              |
| - setActive                                  |
+----------------------------------------------+
                      |
                      v
+----------------------------------------------+
|          Database (via Prisma)               |
| (/src/lib/prisma.ts)                         |
| - User verification (if needed)              |
+----------------------------------------------+

Common Elements:
+----------------------------------------------+
|              Form Validation                 |
| - Zod schemas (/src/schemas/auth.schema.ts)  |
| - React Hook Form (useForm, useFormContext)  |
+----------------------------------------------+

+----------------------------------------------+
|            Toast Notifications               |
| (/src/components/ui/use-toast.ts)            |
+----------------------------------------------+

+----------------------------------------------+
|             Next.js Routing                  |
| (useRouter from next/navigation)             |
+----------------------------------------------+

+----------------------------------------------+
|           Authentication Context             |
| (/src/context/use-auth-context.ts)           |
| - Manages authentication state               |
+----------------------------------------------+


NPM commands
npm install axios 
npm add html-react-parser for actions/landing/index.ts

File Upload:
-- npm i @uploadcare/react-uploader

pusher
npm i pusher
npm i pusher-js

nodemailer
npm i nodemailer
npm i --save-dev @types/nodemailer

OpenAI
npm install openai

Stripe
npm install stripe
npm install @stripe/react-stripe-js @stripe/stripe-js


