// import { onGetBlogPosts } from '@/actions/landing'
// import NavBar from '@/components/navbar'
// import { Button } from '@/components/ui/button'
// import {
//   Card,
//   CardContent,
//   CardDescription,
//   CardFooter,
//   CardHeader,
//   CardTitle,
// } from '@/components/ui/card'
// import { pricingCards } from '@/constants/landing-page'
// import clsx from 'clsx'
// import { ArrowRightCircleIcon, Check } from 'lucide-react'
// import Image from 'next/image'
// import Link from 'next/link'
// import parse from "html-react-parser"
// import { getMonthName } from '@/lib/utils'


// export default async function Home() {
//   //need to complete the billing card remember
//   const posts:
//   | {
//       id: string
//       title: string
//       image: string
//       content: string
//       createdAt: Date
//     }[]
//   | undefined = await onGetBlogPosts()

//   return (
//     <main>
//       <NavBar />
//       {/* Hero Section */}
//       <section>
//         <div className="flex items-center justify-center flex-col mt-[80px] gap-4 px-4 md:px-0">
//           <span className="text-orange bg-orange/20 px-4 py-2 rounded-full text-sm text-center">
//           An AI-powered sales assistant chatbot and lead generation tool
//           </span>
//           <Image
//             src="/images/logo.png"
//             width={500}
//             height={100}
//             alt="Logo"
//             className="max-w-full md:max-w-lg object-contain"
//           />
//           <p className="text-center max-w-[500px] text-sm md:text-base">
//           4X your revenue with Amplifier AI – an AI-powered sales assistant and lead generation tool. 
//           Easily embed it into any website with just a snippet of code!
//           </p>
//           <Button className="bg-orange font-bold text-white px-6 py-2 rounded-md">
//             Start Here
//           </Button>
//           <Image
//             src="/images/desktopamplifier.png"
//             width={800}
//             height={200}
//             alt="Logo"
//             className="max-w-full w-full md:max-w-4xl object-contain mt-4"
//           />
//         </div>
//       </section>

//       {/* Pricing Section */}
//       <section className="flex justify-center items-center flex-col gap-4 mt-10 px-4 md:px-0">
//         <h2 className="text-2xl md:text-4xl text-center"> Choose what fits you right</h2>
//         <p className="text-muted-foreground text-center max-w-lg text-sm md:text-base">
//           Our straightforward pricing plans are tailored to meet your needs. If
//           {" you're"} not ready to commit you can get started for free.
//         </p>
//       </section>

//       {/* Pricing Cards */}
//       <div className="flex flex-col md:flex-row justify-center gap-4 flex-wrap mt-6 px-4 md:px-0">
//         {pricingCards.map((card) => (
//           <Card
//             key={card.title}
//             className={clsx('w-full md:w-[300px] flex flex-col justify-between', {
//               'border-2 border-primary': card.title === 'Unlimited',
//             })}
//           >
//             <CardHeader>
//               <CardTitle className="text-orange">{card.title}</CardTitle>
//               <CardDescription>
//                 {pricingCards.find((c) => c.title === card.title)?.description}
//               </CardDescription>
//             </CardHeader>
//             <CardContent>
//               <span className="text-4xl font-bold">{card.price}</span>
//               <span className="text-muted-foreground">
//                 <span>/ month</span>
//               </span>
//             </CardContent>
//             <CardFooter className="flex flex-col items-start gap-4">
//               <div>
//                 {card.features.map((feature) => (
//                   <div
//                     key={feature}
//                     className="flex gap-2 items-center"
//                   >
//                     <Check />
//                     <p>{feature}</p>
//                   </div>
//                 ))}
//               </div>
//               <Link
//                 href={`/dashbord?plan=${card.title}`}
//                 className="bg-[#f3d299] border-orange border-2 p-2 w-full text-center font-bold rounded-md"
//               >
//                 Get Started
//               </Link>
//             </CardFooter>
//           </Card>
//         ))}
//       </div>

//       <section className="flex justify-center items-center flex-col gap-4 mt-28">
//         <h2 className="text-4xl text-center">News Room</h2>
//         <p className="text-muted-foreground text-center max-w-lg">
//           Explore our insights on AI, technology, and optimizing your business.
//         </p>
//       </section>
//       <section className="md:grid-cols-3 grid-cols-1 grid gap-5 container mt-8">
//         {posts &&
//           posts.map((post) => (
//             <Link
//               href={`/blogs/${post.id}`}
//               key={post.id}
//             >
//               <Card className="flex flex-col gap-2 rounded-xl overflow-hidden h-full hover:bg-gray-100">
//                 <div className="relative w-full aspect-video">
//                   <Image
//                     src={`${process.env.CLOUDWAYS_UPLOADS_URL}${post.image}`}
//                     alt="post featured image"
//                     fill
//                   />
//                 </div>
//                 <div className="py-5 px-10 flex flex-col gap-5">
//                   <CardDescription>
//                     {getMonthName(post.createdAt.getMonth())}{' '}
//                     {post.createdAt.getDate()} {post.createdAt.getFullYear()}
//                   </CardDescription>
//                   <CardTitle>{post.title}</CardTitle>
//                   {parse(post.content.slice(4, 100))}...
//                 </div>
//               </Card>
//             </Link>
//           ))}
//       </section>
//     </main>
//   )
// }

import { onGetBlogPosts } from '@/actions/landing'
import NavBar from '@/components/navbar'
import { Button } from '@/components/ui/button'
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from '@/components/ui/card'
import { pricingCards } from '@/constants/landing-page'
import clsx from 'clsx'
import { ArrowRightCircle, Check, ChevronRight } from 'lucide-react'
import Image from 'next/image'
import Link from 'next/link'
import parse from "html-react-parser"
import { getMonthName } from '@/lib/utils'

export default async function Home() {
  const posts = await onGetBlogPosts()

  return (
    <main className="bg-gradient-to-b from-background to-secondary/10">
      <NavBar />
      
      {/* Hero Section */}
      <section className="container mx-auto px-4 py-20 md:py-32">
        <div className="flex flex-col items-center text-center gap-8">
        <span className="inline-block bg-orange/20 text-orange px-6 py-2 rounded-full text-sm font-bold">
         AI-powered Sales Assistant & Lead Generation
        </span>
          <Image
            src="/images/logo.png"
            width={500}
            height={100}
            alt="Logo"
            className="max-w-full md:max-w-lg object-contain"
          />
          <h1 className="text-4xl md:text-6xl font-bold tracking-tight">
            Get more Customers with <span className="text-orange">Amplifier AI</span>
          </h1>
          <p className="max-w-[600px] text-lg text-muted-foreground">
            Easily embed our AI-powered sales assistant and lead generation tool into any website with just a snippet of code!
          </p>
          <Button className="bg-orange text-white px-8 py-6 text-lg rounded-full transition-all duration-300 shadow-lg hover:shadow-xl">
            Get Started Now <ChevronRight className="ml-2" />
          </Button>
          <div className="relative w-full max-w-4xl mt-12 rounded-lg overflow-hidden shadow-2xl">
            <Image
              src="/images/desktopamplifier.png"
              width={800}
              height={200}
              alt="Amplifier AI Dashboard"
              className="w-full object-cover"
            />
            <div className="absolute inset-0 bg-gradient-to-t from-black/50 to-transparent"></div>
          </div>
        </div>
      </section>

      {/* Pricing Section */}
      <section className="flex justify-center items-center flex-col gap-4 mt-10 px-4 md:px-0"> 
        <div className="container mx-auto px-4">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-5xl font-bold mb-4">Choose Your Perfect Plan</h2>
            <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
              Our straightforward pricing plans are tailored to meet your needs. If {"you're"} not ready to commit, you can get started for free.
            </p>
          </div>
          
          <div className="grid md:grid-cols-3 gap-8">
            {pricingCards.map((card) => (
              <Card
                key={card.title}
                className={clsx('flex flex-col justify-between transition-all duration-300 hover:shadow-xl', {
                  'border-2 border-orange scale-105': card.title === 'Unlimited',
                })}
              >
                <CardHeader>
                  <CardTitle className="text-2xl font-bold text-orange">{card.title}</CardTitle>
                  <CardDescription className="text-lg">{card.description}</CardDescription>
                </CardHeader>
                <CardContent>
                  <span className="text-5xl font-bold">{card.price}</span>
                  <span className="text-xl text-muted-foreground ml-2">/ month</span>
                </CardContent>
                <CardFooter className="flex flex-col items-start gap-4">
                  <ul className="space-y-2 mb-6">
                    {card.features.map((feature) => (
                      <li key={feature} className="flex items-center gap-2">
                        <Check className="text-green-500" />
                        <span>{feature}</span>
                      </li>
                    ))}
                  </ul>
                  <Link
                    href={`/dashboard?plan=${card.title}`}
                    className="bg-[#f3d299] border-orange border-2 p-2 w-full text-center font-bold rounded-md"
                  >
                    Get Started
                  </Link>
                </CardFooter>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* News Room Section */}
      <section className="py-20">
        <div className="container mx-auto px-4">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-5xl font-bold mb-4">News Room</h2>
            <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
              Explore our insights on AI, technology, and optimizing your business.
            </p>
          </div>
          
          <div className="grid md:grid-cols-3 gap-8">
            {posts && posts.map((post) => (
              <Link href={`/blogs/${post.id}`} key={post.id} className="group">
                <Card className="overflow-hidden h-full transition-all duration-300 hover:shadow-lg group-hover:-translate-y-2">
                  <div className="relative w-full aspect-video">
                    <Image
                      src={`${process.env.CLOUDWAYS_UPLOADS_URL}${post.image}`}
                      alt={post.title}
                      fill
                      className="object-cover"
                    />
                  </div>
                  <CardContent className="p-6">
                    <CardDescription className="text-sm mb-2">
                      {getMonthName(post.createdAt.getMonth())} {post.createdAt.getDate()}, {post.createdAt.getFullYear()}
                    </CardDescription>
                    <CardTitle className="text-xl mb-4 group-hover:text-orange transition-colors duration-300">{post.title}</CardTitle>
                    <div className="text-muted-foreground">
                      {parse(post.content.slice(0, 150))}...
                    </div>
                  </CardContent>
                  <CardFooter className="p-6 pt-0">
                    <Button variant="link" className="p-0 h-auto font-semibold group-hover:text-orange">
                      Read More <ArrowRightCircle className="ml-2 w-4 h-4" />
                    </Button>
                  </CardFooter>
                </Card>
              </Link>
            ))}
          </div>
        </div>
      </section>
    </main>
  )
}