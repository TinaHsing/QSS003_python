
#include <stdio.h>   
#include <dlfcn.h> 
#include <stdlib.h>  
  
int main(void){   
   int (*myadd)();//fuction pointer   
   void *handle;   
      
   handle=dlopen("/home/pi/QSS003_python/libhello.so",RTLD_LAZY);//open lib file   
    if(!handle)
    {
        printf("%s \n",dlerror());
        exit(1);
    }
   myadd=dlsym(handle,"Hello");//call dlsym function   
      
   myadd();   
   dlclose(handle);   
}