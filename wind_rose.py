####################################################################
# скрипт должен лежать в директории запуска терминала по умолчанию #
# или придется прописывать полный путь до файла                    #
# Пример команды для запуска скрипта с вашими значениями -         #
# python wind_rose.py --n_kph 1 --ne_kph 2 --e_kph 3 --se_kph 4    #
# --s_kph 5 --sw_kph 6--w_kph 7 --nw_kph 8 --format svg --show 1   #
# Пример команды для запуска скрипта для теста -                   #
# python wind_rose.py                                              #
####################################################################
rose = '''
                                                5@@5                                                
                                               J@@@@?                                               
                                              ^&@@@@&^                                              
                                              G@@@@@@G                                              
                                             ?@@@@@@@@?                                             
                                            ^&@@@@@@@@&^                                            
                                            G@@@@@@@@@@P                                            
                                           ?@@@B&@@&B@@@?                                           
                    :                     :&@@&~#@@#~&@@&^                     :                    
                   5&&BY7:                P@@@J &@@& J@@@P                ^!YB&&5                   
                   Y@@@@@&BY7:           7@@@G  &@@&: B@@@7           ^!YB&@@@@@J                   
                    ?@@@@@@@@@BY!^      :&@@@~  &@@&: ~@@@&:      :75B@@@@@@@@@?                    
                     7@@@@5JG&@@@@BY!^  P@@@J  :&@@&   Y@@@P  ^75B@@@@&BY5@@@@!                     
                      ~&@@&7 :!YG&@@@@BP@@@B   :&@@&    B@@@PB@@@@&BY!: 7&@@&~                      
                       ^#@@@J    :7YB&@@@@@~    &@@&:   ~@@@@@&GY!:    J@@@#~                       
                        :B@@@Y       :B@@@Y     &@@&:    Y@@@B:       5@@@B:                        
                          P@@@P:     !@@@B     :&@@&     :B@@@!      P@@@G:                         
                           5@@@G^:^!J#@@@!     :&@@&      !@@@#J7~::G@@@5                           
                          :~B@@@&&@@@@@@@B7     &@@&:    7B@@@@@@@&&@@@B^                           
                   :~!?5G#&@@@@@@#G5J7?#@@@B?   &@@&   ?B@@@B?7J5G#&@@@@@&#G5J7^:                   
            :~!J5GB&@@@@@@#G5J7~^       7B@@@#J^#@@#^?#@@@B7       :~7JPB#@@@@@@&#G5?!^:            
     :^!?YPB&@@@@@&#G5J!^:                !P@@@&@@@@&@@@P~                :~7J5G#&@@@@@&BG5?!^:     
^?YPB&@@@@@@@@@&BPYJ?777????????????????????P@@@@@@@@@@P?7??????????????????????JYPB&@@@@@@@@@&BPY7:
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@B
^7YPB&@@@@@@@@@&BPYJ??????????????????????7?P@@@@@@@@@@P????????????????????777?JYPB&@@@@@@@@@&BPY?^
      ^!?5GB&@@@@@&#G5J7~:                ~P@@@&@@@@&@@@G!                :^!J5G#&@@@@@&BPY?!^:     
            :^!?5G#&@@@@@@#BPJ7~:       7B@@@#?^#@@#^J#@@@B7       ^~7J5G#@@@@@@&BG5J!~:            
                   :^7J5G#&@@@@@&#G5J7?B@@@B?   &@@&   ?B@@@B?7J5G#@@@@@@&#G5?!~:                   
                           ^B@@@&&@@@@@@@B7    :&@@&     7B@@@@@@@&&@@@B~:                          
                           5@@@G::~7J#@@@!     :&@@&:     !@@@#J!^:^G@@@5                           
                         :G@@@P      !@@@B:     &@@&:     B@@@!     :P@@@P                          
                        :B@@@5       :B@@@Y    :&@@&     Y@@@B:       Y@@@B:                        
                       ~#@@@J    :!YG&@@@@@~   :&@@&    ~@@@@@&BY7:    J@@@#^                       
                      ~&@@&7 :!YB&@@@@BP@@@B    &@@&:   B@@@PB@@@@&GY!: 7&@@&~                      
                     !@@@@5YB&@@@@B57^  P@@@Y   &@@&:  J@@@P  ^!YB@@@@&GJ5@@@@7                     
                    ?@@@@@@@@@B57:      :&@@@~ :&@@&  ~@@@&:      ^!YB@@@@@@@@@?                    
                   J@@@@@&BY!^           7@@@G :&@@&  G@@@7           :7YB&@@@@@Y                   
                   5&&BY!^                P@@@J &@@& J@@@P                :7YB&&5                   
                    :                     ^&@@&~#@@#!&@@&:                    :                     
                                           ?@@@B&@@&B@@@?                                           
                                            P@@@@@@@@@@G                                            
                                            ^&@@@@@@@@&^                                            
                                             ?@@@@@@@@?                                             
                                              G@@@@@@G                                              
                                              ^&@@@@&^                                              
                                               ?@@@@J                                               
                                                5@@5                                                '''
# стадартные импорты встроенных библиотек
import click 
import warnings
import math as m
from math import pi
import matplotlib.pyplot as plt

# Глушим warning FixedFormatter следует использовать только вместе с FixedLocator
# Да костыль, ну и чёрт с ним.
warnings.filterwarnings("ignore")

# порядок значений angles_grad c.св.в.юв.ю.юз.з.сз 
angles_grad = [0,45,90,135,180,225,270,315]

# список меток сторон света
pointx_names = ['С','СЗ','З','ЮЗ','Ю','ЮВ','В','СВ']

# список меток скорости ветра
pointy_names = ['1 км.ч','2 км.ч','3 км.ч','4 км.ч','5 км.ч',
                '6 км.ч','7 км.ч','8 км.ч','9 км.ч','10 км.ч',
                '11 км.ч','12 км.ч','13 км.ч','14 км.ч','15 км.ч',
                '16 км.ч','17 км.ч','18 км.ч','19 км.ч','20 км.ч',
                '21 км.ч','22 км.ч','23 км.ч','24 км.ч','25 км.ч',
                '26 км.ч','27 км.ч','28 км.ч','29 км.ч','30 км.ч',
                '31 км.ч','32 км.ч','33 км.ч','34 км.ч','35 км.ч',
                '36 км.ч','37 км.ч','38 км.ч','39 км.ч','40 км.ч',]

# функция переводит градусы углов в радианы полярного графика 
def grad_to_radian(angles_grad):
    angles_rad = []
    for i in angles_grad:
        rad = m.radians(i)
        angles_rad.append(rad)
    return angles_rad
# печать огромной розы в cli
click.echo(rose)
# С помощию библиотеки click создаем cli интерфейс командной строки
@click.command(help='''Скрипт принимает упорядоченные данные о скорости ветра в километрах в час, 
формат файла и занчение для вывода графика в окне.
Доступны форматы: 
eps, jpeg, jpg, pdf, pgf, png, ps, raw, rgba, svg, svgz, tif, tiff, webp.
''')


# аргумент скорости ветра для ветра с севера
@click.option('--n_kph',default=1,type=click.INT,
help='wind speed from north')

# аргумент скорости ветра для ветра с северо-запада
@click.option('--ne_kph',default=2,type=click.INT,
help='wind speed from north-east')

# аргумент скорости ветра для ветра с запада
@click.option('--e_kph',default=3,type=click.INT,
help='wind speed from east')

# аргумент скорости ветра для ветра с юго-запада
@click.option('--se_kph',default=4,type=click.INT,
help='wind speed from south-east')

# аргумент скорости ветра для ветра с юга
@click.option('--s_kph',default=5,type=click.INT,
help='wind speed from south')

# аргумент скорости ветра для ветра с юго-востока
@click.option('--sw_kph',default=6,type=click.INT,
help='wind speed from south-west')

#аргумент скорости ветра для ветра с востока
@click.option('--w_kph',default=7,type=click.INT,
help='wind speed from west')

# аргумент скорости ветра для ветра с северо-востока
@click.option('--nw_kph',default=8,type=click.INT,
help='wind speed from north-west')

# аргумент для вывода графика в окне
@click.option('--show',default=1,type=click.INT,
help='sowh window with diagram or not')

# аргумент с форматом выходного файла с графиком, по умолчанию png
@click.option('--format',default='png',type=click.STRING,
help='format output file, suported: svg,pdf,png')

# аргумент для установки фона png, по умолчанию не прозрачный
@click.option('--background',default=1,type=click.INT,
help='1 - with white background 0 - with transparent background ')

# функция принимает данные из cli и создает полярный график розы ветров
def graphics_build(n_kph,ne_kph,e_kph,se_kph,s_kph,sw_kph,w_kph,nw_kph,format,show,background):
    kph = [n_kph,ne_kph,e_kph,se_kph,s_kph,sw_kph,w_kph,nw_kph]
    #  Строим полярный график
    # создание холста
    fig = plt.figure(figsize=(4.1,4.1)) 

    # создание слоя с полярным графиком
    ax = fig.add_subplot(111, projection='polar')

    # отрисовка точек и линий на полярном графике
    ax.plot(grad_to_radian(angles_grad), kph , color='gray', linewidth=2,alpha=0.1,solid_capstyle='round')

    # (соединяем конец и начало с нулевыми точками графика)
    ax.plot((grad_to_radian(angles_grad)[-1],grad_to_radian(angles_grad)[0]),(kph[-1],kph[0]),
     color='gray', linewidth=2,alpha=0.1,solid_capstyle='round')

    # заливаем внутренний полигон графика
    ax.fill(grad_to_radian(angles_grad), kph,color='blue',alpha=0.2)
    
    # переименовываем градусы в стороны света
    ax.set_xticklabels(pointx_names,color='black',fontweight ="bold")
    ax.set_yticklabels(pointy_names,color='black')
    # Построение графика "по часовой"
    ax.set_theta_direction(-1)

    # Смещаем нулевую или полярную ось в положение "север"
    ax.set_theta_offset(pi/2.0)

    # Название графика
    ax.set_title(u"Направление ветра", loc='center')

    # сохраняем файл с графиком
    if background == 1:
        plt.savefig(f'wind_rose.{format}')
    if background == 0:
        plt.savefig(f'wind_rose.{format}',transparent= True)
    
    # вывод графика в окне
    if show == 1:
        plt.show()


# Традиционный запуск самостоятельного скрипта Python
if __name__ == '__main__':
    graphics_build()