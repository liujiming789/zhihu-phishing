#include "stm32f2xx.h"
#include "sys.h"
#include "lcd.h"
#include "delay.h"
#include "stdio.h"
#include "stdlib.h"
#include "stm32f2xx_it.h"
#include "math.h"
#include "time.h"
#include "stdlib.h"

void  TOUCH_SCREEN_INIT();
u32 SPI_X(void);
u32 SPI_Y(void);
static void TOUCH_INT_config(void);
static void TOUCH_INT_EXIT_Init(void);
static void TOUCH_InterruptConfig(void);
int Max(int a,int b);
int Min(int a,int b);
void Kill_a_chess(int i,int j);
void Kill(int i,int j);
static void LCD_BIG_POINT(u16 x, u16 y);
void TouchScreen();
void Draw_chessboard();
void Run_astep(int x,int y,int i,int j,int color);

uint16_t color[8] = {BLUE,BRED,GRED,GBLUE,RED,MAGENTA,GREEN,YELLOW};
u8 num;
#define  times  4
u16 x_addata[times],z_addata[times],y_addata[times];
u32 Temp ,r,sx,sy= 0;
int  SW=0,sw=0,sum=0,I=0,J=0;   //黑白棋转换
int  Chessman[5][7];
int time_sum = 0;
int sum_times = 0;
int ii=0,jj=0;

u8 delay_time;
u8 count=0;	 

void TIM2_IRQHandler(void)
{

	if (TIM_GetITStatus(TIM2, TIM_IT_Update) != RESET)  //检查标志位
	{
		count++;

		TIM_ClearITPendingBit(TIM2, TIM_IT_Update);  //清除标志位	
	}
	if(count==20)
	{
		delay_time=1;
		count=0;
	}
}

int main(void)
{ 
		TOUCH_SCREEN_INIT();
		LCD_Init();

		tim_init();

		
		TOUCH_INT_config();
		TOUCH_INT_EXIT_Init();
		TOUCH_InterruptConfig();
		
		Draw_chessboard();
		while  (1)
		{   
		}
}

void  TOUCH_SCREEN_INIT()
{ 
	
	   GPIO_InitTypeDef GPIO_InitStructure;
	   SPI_InitTypeDef  SPI_InitStructure;
  /* Enable GPIOB, GPIOC and AFIO clock */
     RCC_APB2PeriphClockCmd(RCC_APB2Periph_SPI1,ENABLE);
     RCC_AHB1PeriphClockCmd(RCC_AHB1Periph_GPIOA|RCC_AHB1Periph_GPIOB , ENABLE);  //RCC_APB2Periph_AFIO
 //  GPIO_PinAFConfig(GPIOA, GPIO_PinSource15, GPIO_AF_SPI1); //nss 
     GPIO_PinAFConfig(GPIOA, GPIO_PinSource5, GPIO_AF_SPI1 ); //sck
     GPIO_PinAFConfig(GPIOA, GPIO_PinSource6, GPIO_AF_SPI1 ); //miso
     GPIO_PinAFConfig(GPIOB, GPIO_PinSource5, GPIO_AF_SPI1 ); //mosi 
  /* LEDs pins configuration */
     GPIO_InitStructure.GPIO_Pin = GPIO_Pin_15 ;
		 GPIO_InitStructure.GPIO_Speed = GPIO_Speed_50MHz;
     GPIO_InitStructure.GPIO_Mode = GPIO_Mode_OUT;
     GPIO_InitStructure.GPIO_OType = GPIO_OType_PP;
     GPIO_Init(GPIOA, &GPIO_InitStructure);


     GPIO_InitStructure.GPIO_Mode = GPIO_Mode_AF;
     GPIO_InitStructure.GPIO_Speed = GPIO_Speed_50MHz; // also 100Mhz
     GPIO_InitStructure.GPIO_OType = GPIO_OType_PP;
     GPIO_InitStructure.GPIO_PuPd  = GPIO_PuPd_UP; // GPIO_PuPd_DOWN
     GPIO_InitStructure.GPIO_Pin = GPIO_Pin_6 | GPIO_Pin_5 ;
     GPIO_Init(GPIOA, &GPIO_InitStructure);// SCK,MISO   
     GPIO_InitStructure.GPIO_Mode = GPIO_Mode_AF;
     GPIO_InitStructure.GPIO_Speed = GPIO_Speed_50MHz; // also 100Mhz
     GPIO_InitStructure.GPIO_OType = GPIO_OType_PP;
     GPIO_InitStructure.GPIO_PuPd  = GPIO_PuPd_UP; // GPIO_PuPd_DOWN
     GPIO_InitStructure.GPIO_Pin =  GPIO_Pin_5;
     GPIO_Init(GPIOB, &GPIO_InitStructure);// MOSI
   	 SPI_InitStructure.SPI_Direction = SPI_Direction_2Lines_FullDuplex;//SPI??????????
     SPI_InitStructure.SPI_Mode = SPI_Mode_Master;//????SPI
     SPI_InitStructure.SPI_DataSize = SPI_DataSize_8b;//??SPI?????:SPI????8????
     SPI_InitStructure.SPI_CPOL = SPI_CPOL_Low;//??????????:?????
     SPI_InitStructure.SPI_CPHA = SPI_CPHA_1Edge;//???????????
     SPI_InitStructure.SPI_NSS = SPI_NSS_Soft;//(SPI_NSS_Soft)??NSS?????????GPIO??????
     SPI_InitStructure.SPI_BaudRatePrescaler = SPI_BaudRatePrescaler_256;//Fclk/2
     SPI_InitStructure.SPI_FirstBit = SPI_FirstBit_MSB; /* Initialize the SPI_FirstBit member */
     SPI_InitStructure.SPI_CRCPolynomial=7;
     SPI_Init(SPI1, &SPI_InitStructure);
     SPI_Cmd(SPI1, ENABLE);

}
//定位x
u32 SPI_X(void) 
{ 

   u16		i,j,k;
     GPIO_ResetBits(GPIOA,GPIO_Pin_15);
	   for(i=0;i<times;i++)					//采样4次.
	     {

				SPI_I2S_SendData(SPI1, 0xD0);
		    while (SPI_I2S_GetFlagStatus(SPI1, SPI_I2S_FLAG_TXE) == RESET); 
		    SPI_I2S_SendData(SPI1, 0);
		    while (SPI_I2S_GetFlagStatus(SPI1, SPI_I2S_FLAG_TXE) == RESET); 
			  SPI_I2S_SendData(SPI1, 0);
				z_addata[i]=SPI_I2S_ReceiveData(SPI1);
		    while (SPI_I2S_GetFlagStatus(SPI1, SPI_I2S_FLAG_TXE) == RESET); 
        x_addata[i]=SPI_I2S_ReceiveData(SPI1);
		    x_addata[i]<<=8;	
			  while (SPI_I2S_GetFlagStatus(SPI1, SPI_I2S_FLAG_RXNE) == RESET);
	    	x_addata[i]|=SPI_I2S_ReceiveData(SPI1);
        x_addata[i]>>=3;


			}  
    GPIO_SetBits(GPIOA,GPIO_Pin_15); 
			
	  for(i=0;i<times;i++)
		{
			for(j=times;j<times-1;j++)
				{
					 if(x_addata[j] > x_addata[i])
						{
							k = x_addata[i];
							x_addata[i] = x_addata[j];
							x_addata[j] = k;
						}
				}
		 }
			
	 Temp=(x_addata[1] + x_addata[2]) >> 1;
			 
	 r =Temp - 200;
   r *= 240;
   sx=r / (4000 - 200);
   if (sx<=0 || sx>240)
       return 0;
	 sx = ((int)((sx-20)/40)+1)*40;
   return sx;
}

u32 SPI_Y(void) 
{ 

   u16		i,j,k;
   GPIO_ResetBits(GPIOA,GPIO_Pin_15);
	 for(i=0;i<times;i++)					//采样4次.
	{

	  SPI_I2S_SendData(SPI1, 0x90);
		while (SPI_I2S_GetFlagStatus(SPI1, SPI_I2S_FLAG_TXE) == RESET); 
		SPI_I2S_SendData(SPI1, 0);
		while (SPI_I2S_GetFlagStatus(SPI1, SPI_I2S_FLAG_TXE) == RESET); 
		SPI_I2S_SendData(SPI1, 0);
		z_addata[i]=SPI_I2S_ReceiveData(SPI1);
		while (SPI_I2S_GetFlagStatus(SPI1, SPI_I2S_FLAG_TXE) == RESET); 
    y_addata[i]=SPI_I2S_ReceiveData(SPI1);
		y_addata[i]<<=8;	
		while (SPI_I2S_GetFlagStatus(SPI1, SPI_I2S_FLAG_RXNE) == RESET);
		y_addata[i]|=SPI_I2S_ReceiveData(SPI1);
    y_addata[i]>>=3;

	
	}
  GPIO_SetBits(GPIOA,GPIO_Pin_15); 
	for(i=0;i<times;i++)
	  {
      	for(j=times;j<times-1;j++)
    	  {
             if(y_addata[j] > y_addata[i])
              {
                 k = y_addata[i];
                 y_addata[i] = y_addata[j];
                 y_addata[j] = k;
              }
        }
    }
	Temp=(y_addata[1] + y_addata[2]) >> 1;
	r =Temp - 190;
  r *= 320;
  sy=r / (4000 - 190);
  if (sy<=0 || sy>320)
      return 0;
	sy = ((int)((sy-20)/40)+1)*40;
  return sy;
}  
 
static void TOUCH_INT_config(void)
{
     GPIO_InitTypeDef GPIO_InitStructure;
     /* Enable GPIOB, GPIOC and AFIO clock */
     RCC_AHB1PeriphClockCmd(RCC_AHB1Periph_GPIOC , ENABLE);  
     /* LEDs pins configuration */
     GPIO_InitStructure.GPIO_Pin = GPIO_Pin_2;
     //GPIO_InitStructure.GPIO_Speed = GPIO_Speed_50MHz;
     GPIO_InitStructure.GPIO_Mode = GPIO_Mode_IN;
	   GPIO_InitStructure.GPIO_PuPd  = GPIO_PuPd_UP;
     GPIO_Init(GPIOC, &GPIO_InitStructure);
}

static void TOUCH_INT_EXIT_Init(void)
{
     EXTI_InitTypeDef EXTI_InitStructure;
     RCC_APB2PeriphClockCmd(RCC_APB2Periph_SYSCFG , ENABLE);
    /* Connect Button EXTI Line to Button GPIO Pin */
     SYSCFG_EXTILineConfig(EXTI_PortSourceGPIOC,EXTI_PinSource2);

    /* Configure Button EXTI line */
     EXTI_InitStructure.EXTI_Line = EXTI_Line2;
     EXTI_InitStructure.EXTI_Mode = EXTI_Mode_Interrupt;
     EXTI_InitStructure.EXTI_Trigger = EXTI_Trigger_Falling;  
     EXTI_InitStructure.EXTI_LineCmd = ENABLE;
     EXTI_Init(&EXTI_InitStructure);
	   EXTI_ClearITPendingBit(EXTI_Line2);
	

	}
static void TOUCH_InterruptConfig(void)
{ 
    NVIC_InitTypeDef NVIC_InitStructure;
  
  /* Set the Vector Table base address at 0x08000000 */
    NVIC_SetVectorTable(NVIC_VectTab_FLASH, 0x0000);
 /* Configure the Priority Group to 2 bits */
    NVIC_PriorityGroupConfig(NVIC_PriorityGroup_2);

    NVIC_InitStructure.NVIC_IRQChannel = EXTI2_IRQn;
    NVIC_InitStructure.NVIC_IRQChannelPreemptionPriority = 0;
    NVIC_InitStructure.NVIC_IRQChannelSubPriority = 0;
    NVIC_InitStructure.NVIC_IRQChannelCmd = ENABLE;
    NVIC_Init(&NVIC_InitStructure);
}

int Max(int a,int b)
{
	if(a>b)
	{
		return a;
	}
	else
		return b;
}
int Min(int a,int b)
{
	if(a>b)
	{
		return b;
	}
	else
		return a;
}

void Kill_a_chess(int i,int j)
{
	if(i>=0 && i<5 && j>=0 && j<7)
	{
			u16 x = 40*(i+1);
			u16 y = 40*(j+1);
			 LCD_Draw_Circle(x,y,10,1,YELLOW);
			 LCD_Color_Fill(x,Max(40,y-20),x,Min(y+20,280),BLACK);
			 LCD_Color_Fill(Max(40,x-20),y,Min(x+20,200),y,BLACK);
			Chessman[i][j] = 0;	
	}
}

 void Kill(int i,int j)
 {
	 //Killed
	 if(i+2<5)
		 if(Chessman[i+1][j]==-Chessman[i][j] && Chessman[i+2][j]==-Chessman[i][j]) Kill_a_chess(i,j);
	 if(j+2<7)
		 if(Chessman[i][j+1]==-Chessman[i][j] && Chessman[i][j+2]==-Chessman[i][j]) Kill_a_chess(i,j);
	 if(i-2>=0)
		 if(Chessman[i-1][j]==-Chessman[i][j] && Chessman[i-2][j]==-Chessman[i][j]) Kill_a_chess(i,j);
	 if(j-2>=0)
		 if(Chessman[i][j-1]==-Chessman[i][j] && Chessman[i][j-2]==-Chessman[i][j]) Kill_a_chess(i,j);
	 
	 //Kill
	 if(i+1<5)
		 if(Chessman[i+1][j]==Chessman[i][j]){if(Chessman[i-1][j]==-Chessman[i][j])Kill_a_chess(i-1,j);if(Chessman[i+2][j]==-Chessman[i][j])Kill_a_chess(i+2,j);}
	 if(j+1<7)
		 if(Chessman[i][j+1]==Chessman[i][j]){if(Chessman[i][j-1]==-Chessman[i][j])Kill_a_chess(i,j-1);if(Chessman[i][j+2]==-Chessman[i][j])Kill_a_chess(i,j+2);}
	 if(i-1>=0)
		 if(Chessman[i-1][j]==Chessman[i][j]){if(Chessman[i-2][j]==-Chessman[i][j])Kill_a_chess(i-2,j);if(Chessman[i+1][j]==-Chessman[i][j])Kill_a_chess(i+1,j);}
	 if(j-1>=0)
		 if(Chessman[i][j-1]==Chessman[i][j]){if(Chessman[i][j-2]==-Chessman[i][j])Kill_a_chess(i,j-2);if(Chessman[i][j+1]==-Chessman[i][j])Kill_a_chess(i,j+1);}
}
 
int  Killtest(int i,int j)
 {
	 int S=0;
	 //Killed
	 if(i+2<5)
		 if(Chessman[i+1][j]==-Chessman[i][j] && Chessman[i+2][j]==-Chessman[i][j]) S=-1;
	 if(j+2<7)
		 if(Chessman[i][j+1]==-Chessman[i][j] && Chessman[i][j+2]==-Chessman[i][j]) S=-1;
	 if(i-2>=0)
		 if(Chessman[i-1][j]==-Chessman[i][j] && Chessman[i-2][j]==-Chessman[i][j]) S=-1;
	 if(j-2>=0)
		 if(Chessman[i][j-1]==-Chessman[i][j] && Chessman[i][j-2]==-Chessman[i][j]) S=-1;
	 if(S==-1) return S;
	 
	 //Kill
	 if(i+1<5)
		 if(Chessman[i+1][j]==Chessman[i][j]){if(Chessman[i-1][j]==-Chessman[i][j])S=1;;if(Chessman[i+2][j]==-Chessman[i][j])S=1;}
	 if(j+1<7)
		 if(Chessman[i][j+1]==Chessman[i][j]){if(Chessman[i][j-1]==-Chessman[i][j])S=1;if(Chessman[i][j+2]==-Chessman[i][j])S=1;}
	 if(i-1>=0)
		 if(Chessman[i-1][j]==Chessman[i][j]){if(Chessman[i-2][j]==-Chessman[i][j])S=1;if(Chessman[i+1][j]==-Chessman[i][j])S=1;}
	 if(j-1>=0)
		 if(Chessman[i][j-1]==Chessman[i][j]){if(Chessman[i][j-2]==-Chessman[i][j])S=1;if(Chessman[i][j+1]==-Chessman[i][j])S=1;}
	return S;	
}
 

void Run_astep(int I,int J,int i,int j,int color)
{
	int x = (i+1)*40;
	int y = (j+1)*40;
	if(color==-1)
	 {
		 LCD_Draw_Circle(x,y,10,1,BLACK);
		 Chessman[i][j] = -1;
		 sw = -1;
		 SW =0;
		 sum +=1;
		 Delay(100);
		 LCD_Color_Fill(0,0,20,20,WHITE);
		 LCD_Color_Fill(219,299,239,319,YELLOW);
		 Kill_a_chess(I,J);
		 Kill(i,j);
	 }
	 if(color==1)
	 {
		 LCD_Draw_Circle(x,y,10,1,WHITE);
		 Chessman[i][j] = 1;
		 sw = 1;
		 SW = 0;
		 sum +=1;
		 Delay(100);
		 LCD_Color_Fill(219,299,239,319,BLACK);
		 LCD_Color_Fill(0,0,20,20,YELLOW);
		 Kill_a_chess(I,J);
		 Kill(i,j);
	 }
}

		
//对弈程序
static void LCD_BIG_POINT(u16 x, u16 y)
 {
	 int i = (int)(x/40)-1;
	 int j = (int)(y/40)-1;
	 int flag=0;
	 int number = 0;
	 int iii=0,jjj=0,index=0;
	 int  Score[20][5];
	 int flag1=0;
	 
	 //重新选子
	 if(Chessman[i][j] == Chessman[I][J] &&SW!=0 && sum>0)
	 {
		 if(Chessman[I][J]==-1){
			 LCD_Draw_Circle((I+1)*40,(J+1)*40,10,1,BLACK);
			 LCD_Color_Fill(219,299,239,319,BLACK);
			 LCD_Color_Fill(0,0,20,20,YELLOW);
			 LCD_Draw_Circle(x,y,10,1,RED);
			 Chessman[I][J]=-1;
			 I=i;J=j;}
		 else{
			 LCD_Draw_Circle((I+1)*40,(J+1)*40,10,1,WHITE);
			 LCD_Color_Fill(0,0,20,20,WHITE);
			 LCD_Color_Fill(219,299,239,319,YELLOW);
			 LCD_Draw_Circle(x,y,10,1,RED);
			 Chessman[I][J]=1;
			 I=i;J=j;}
	 }
		 
	 //落子
	 else if(Chessman[i][j]==0 && SW != 0)
	 {
		 if(abs(i-I)+abs(j-J)==1)
		{ 
//			 if(SW==-1 && sw!=-1)
//			 {
//				 Run_astep(x,y,i,j,-1);
//			 }
			 
			 if(SW==1 && sw!=1)
			 { 
				 Run_astep(I,J,i,j,1);
			
				 for(ii=0;ii<5;ii++)
				 {
						for(jj=0;jj<7;jj++)
						 {
							 if(Chessman[ii][jj]==-1)
							 {
								 if(ii<4){
								 if(Chessman[ii+1][jj]==0)
									 {
									 Chessman[ii+1][jj]=-1;
									 Chessman[ii][jj]=0;
									 flag = Killtest(ii+1,jj);
									 Chessman[ii+1][jj]=0;
									 Chessman[ii][jj]=-1;
									 
									Score[index][0] = ii;Score[index][1] = jj;Score[index][2] = ii+1;Score[index][3] = jj;Score[index][4] = flag;
									index++;
									}
									}
								 if(jj<5){
								 if(Chessman[ii][jj+1]==0)
									 {
									 Chessman[ii][jj+1]=-1;
									 Chessman[ii][jj]=0;
									 flag = Killtest(ii,jj+1);
									 Chessman[ii][jj+1]=0;
									 Chessman[ii][jj]=-1;
									 
									 	Score[index][0] = ii;Score[index][1] = jj;Score[index][2] = ii;Score[index][3] = jj+1;Score[index][4] = flag;
									 index++;
									}
									}
								 if(ii>0){
								 if(Chessman[ii-1][jj]==0)
									 {
									 Chessman[ii-1][jj]=-1;
									 Chessman[ii][jj]=0;
									 flag = Killtest(ii-1,jj);
									 Chessman[ii-1][jj]=0;
									 Chessman[ii][jj]=-1;
									 
									 	Score[index][0] = ii;Score[index][1] = jj;Score[index][2] = ii-1;Score[index][3] = jj;Score[index][4] = flag;
									 index++;
									}
									}
								 
									if(jj>0){
								 if(Chessman[ii][jj-1]==0)
									 {
									 Chessman[ii][jj-1]=-1;
									 Chessman[ii][jj]=0;
									 flag = Killtest(ii,jj-1);
									 Chessman[ii][jj-1]=0;
									 Chessman[ii][jj]=-1;
									 
									 	Score[index][0] = ii;Score[index][1] = jj;Score[index][2] = ii;Score[index][3] = jj-1;Score[index][4] = flag;
									 index++;
									}
									}
								}}}
				index--;
				flag=-1;
				for(ii=0;ii<=index;ii++)
				{
					if(Score[ii][4]==1) {I =Score[ii][0];J=Score[ii][1];iii = Score[ii][2];jjj=Score[ii][3];flag=1;flag1=1;}
					if(Score[ii][4]==0 && flag1<1) flag=0;
				}
				if(flag == 0) 
				{
					ii = 0;
					flag1=0;
					for(ii=0;ii<=index;ii++)
					{
						if(Score[ii][4]==0) flag1++;
					}
					ii = 0;
					number = count%flag1;
					while(number>-1)
						{
							if(Score[ii][4]==0) number-=1;
							ii++;
						}
					I =Score[ii][0];
					J=Score[ii][1];	
					iii = Score[ii][2];
					jjj=Score[ii][3];
				}
				if(flag == -1) 
				{
					ii = 0;
					number = 2*(count%5);
					while(number>-1)
						{
							if(Score[ii][4]==-1) number-=1;
							ii++;
						}
					I =Score[ii][0];
					J=Score[ii][1];	
					iii = Score[ii][2];
					jjj=Score[ii][3];
				}
			flag1=0;flag=0;index=0;
			 Run_astep(I,J,iii,jjj,-1);
			 SW=0;sw=-1;	 
			 }
		 }
	 }
	 
	 //选子
	 else if(Chessman[i][j]==1 && SW ==0)
	 {
		 if(y>=40 && x<=280 && sum==0)
		 {
			 SW = Chessman[i][j];  //落子颜色
			 LCD_Draw_Circle(x,y,10,1,RED);
			 if(SW==1) LCD_Color_Fill(0,0,20,20,WHITE);
			 else LCD_Color_Fill(219,299,239,319,BLACK);
			 I=i;J=j;
		 }
		 else if(y>=40 && x<=280&&sum>0)
		 {
			 SW = Chessman[i][j];  
			 LCD_Draw_Circle(x,y,10,1,RED);
			 I=i;J=j;
		 }
	 }
 } u32 xScreen, yScreen;

 
 
void TouchScreen()
{


  static u16 sDataX,sDataY;
    
    xScreen = SPI_X();
    yScreen = SPI_Y();
 
    if((xScreen>1)&&(yScreen>1)&&(xScreen<240-1)&&(yScreen<320-1))
       {
       if(!(GPIO_ReadInputDataBit(GPIOC,GPIO_Pin_2)) )
       {
         LCD_BIG_POINT(240-xScreen,yScreen);
       }
       sDataX = xScreen;
       sDataY = yScreen;
  }
}
void EXTI2_IRQHandler (void)
{
	if(EXTI_GetITStatus(EXTI_Line2) != RESET)
  {
     TouchScreen();
     EXTI_ClearITPendingBit(EXTI_Line2);
  }
}

void Draw_chessboard()
{
	int i,j;
	for(i=0;i<5;i++)
	{
		for(j=0;j<7;j++)
		{
			Chessman[i][j]=0;
		}
	}
	//背景 黄色
	LCD_Color_Fill(0,0,239,319,YELLOW);
	//竖线 40-280
	for(i=40;i<239;i+=40)
		LCD_Color_Fill(i,40,i,280,BLACK);
	//横线 40-200
	for(i=40;i<300;i+=40)
		LCD_Color_Fill(40,i,200,i,BLACK);
	//棋子 r=10
	for(i=40;i<=239;i+=40)
	{
		int i_ = (int)(i/40)-1;
		LCD_Draw_Circle(i,40,10,1,WHITE);
		Chessman[i_][0] = 1;
		LCD_Draw_Circle(i,280,10,1,BLACK);
		Chessman[i_][6] = -1;
	}
}

