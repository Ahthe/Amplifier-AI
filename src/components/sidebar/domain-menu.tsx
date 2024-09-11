import { useDomain } from '@/hooks/sidebar/use-domain'
import { cn } from '@/lib/utils'
import React from 'react'
import AppDrawer from '../drawer'
import { Plus } from 'lucide-react'
import { Loader } from '../loader'
import FormGenerator from '../forms/form-generator'
import UploadButton from '../upload-button'
import { Button } from '../ui/button'
import Link from 'next/link'
import Image from 'next/image'

type Props = {
  min?: boolean
  domains:
    | {
        id: string
        name: string
        icon: string | null
      }[]
    | null
    | undefined
}

const DomainMenu = ({ domains, min }: Props) => {
  const { register, onAddDomain, loading, errors, isDomain } = useDomain()

  return (
    <div className={cn('flex flex-col', min ? 'mt-6' : 'mt-3')}>
      <div className="flex items-center justify-between mb-2">
        {!min && <p className="text-xs text-gray-500">DOMAINS</p>}
        <AppDrawer
          description="Add your domain address to integrate your chatbot"
          title="Add Business Domain"
          //WIP: changed the div container to button for the sake of simplicity (DOnt use it in production)}
          onOpen={
          <div className="inline-flex items-center justify-center w-10 h-10 rounded-md border border-input bg-background hover:bg-accent hover:text-accent-foreground"> 
            <Plus className="h-4 w-4" />
          </div>
          }
        >
          <Loader loading={loading}>
            <form
              className="mt-3 w-6/12 flex flex-col gap-3"
              onSubmit={onAddDomain}
            >
              <FormGenerator
                inputType="input"
                register={register}
                label="Domain"
                name="domain"
                errors={errors}
                placeholder="mydomain.com"
                type="text"
              />
              <UploadButton
                register={register}
                label="Upload Icon"
                errors={errors}
              />
              <Button
                type="submit"
                className="w-full"
              >
                Add Domain
              </Button>
            </form>
          </Loader>
        </AppDrawer>
        </div>
      <div className="space-y-1">
        {domains?.map((domain) => (
          <Link
            key={domain.id}
            href={`/settings/${domain.name.split('.')[0]}`}
            className={cn(
              'flex items-center gap-2 p-2 rounded-lg transition-colors',
              'hover:bg-gray-100 dark:hover:bg-gray-800',
              domain.name.split('.')[0] === isDomain && 'bg-gray-100 dark:bg-gray-800'
            )}
          >
            <Image
              src={`https://ucarecdn.com/${domain.icon}/`}
              alt={domain.name}
              width={24}
              height={24}
              className="rounded-full"
            />
            {!min && <span className="text-sm truncate">{domain.name}</span>}
          </Link>
        ))}
      </div>
    </div>
  )
}
export default DomainMenu