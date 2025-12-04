'use client';

import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import * as z from 'zod';
import { motion } from 'framer-motion';
import toast from 'react-hot-toast';
import { useRouter } from 'next/navigation';
import Link from 'next/link';

import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import useAuthStore from '@/store/useAuthStore';
import apiClient from '@/libraries/apiClient';

const loginSchema = z.object({
  email: z.string().email({ message: 'Неверный адрес электронной почты' }),
  password: z.string().min(6, { message: 'Пароль должен содержать не менее 6 символов' }),
});

type LoginFormValues = z.infer<typeof loginSchema>;

const LoginPage = () => {
  const router = useRouter();
  const { login } = useAuthStore();
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<LoginFormValues>({
    resolver: zodResolver(loginSchema),
  });

  const onSubmit = async (data: LoginFormValues) => {
    try {
      const formData = new URLSearchParams();
      formData.append('username', data.email);
      formData.append('password', data.password);

      const response = await apiClient.auth.login(formData);

      const { access_token } = response.data;
      login(access_token);
      toast.success('Вы успешно вошли в систему!');
      router.push('/matches');
    } catch (error: any) {
      toast.error(error.response?.data?.detail || 'Произошла ошибка при входе в систему.');
    }
  };

  return (
    <div className="flex items-center justify-center min-h-screen">
      <motion.div initial={{ opacity: 0, y: -20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.5 }}>
        <Card className="w-full max-w-sm">
          <CardHeader>
            <CardTitle className="text-2xl">Вход</CardTitle>
            <CardDescription>Введите свою почту ниже, чтобы войти в свой аккаунт.</CardDescription>
          </CardHeader>
          <form onSubmit={handleSubmit(onSubmit)}>
            <CardContent className="grid gap-4">
              <div className="grid gap-2">
                <Label htmlFor="email">Почта</Label>
                <Input id="email" type="email" placeholder="m@example.com" {...register('email')} />
                {errors.email && <p className="text-red-500 text-sm">{errors.email.message}</p>}
              </div>
              <div className="grid gap-2">
                <Label htmlFor="password">Пароль</Label>
                <Input id="password" type="password" {...register('password')} />
                {errors.password && <p className="text-red-500 text-sm">{errors.password.message}</p>}
              </div>
            </CardContent>
            <CardFooter className="flex flex-col">
              <Button type="submit" className="w-full" disabled={isSubmitting}>
                {isSubmitting ? 'Вход...' : 'Войти'}
              </Button>
              <p className="mt-4 text-center text-sm text-muted-foreground">
                Нет аккаунта?{' '}
                <Link href="/register" className="underline">
                  Зарегистрироваться
                </Link>
              </p>
            </CardFooter>
          </form>
        </Card>
      </motion.div>
    </div>
  );
};

export default LoginPage;
