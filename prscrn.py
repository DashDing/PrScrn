from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from time import sleep
def take_scrnshot(address,filename,testmode=False):
    #config
    if testmode:
        print 'set config ...'

    dcap = DesiredCapabilities.PHANTOMJS.copy()
    service_args = ['--config=config.json']
    #firefox
    if testmode:
        print 'init phantomjs ...'
    driver = webdriver.PhantomJS(desired_capabilities=dcap,service_args=service_args)
    driver.set_window_size(1024,768)

    #access and save as pic
    if testmode:
        print 'access and save the {} ...'.format(address)
    driver.implicitly_wait(30)
    driver.get(address)

    #scroll down
    driver.execute_script("""
        (function () {
            var y = 0;
            var step = 100;
            window.scroll(0, 0);

            function f() {
                if (y < document.body.scrollHeight) {
                    y += step;
                    window.scroll(0, y);
                    setTimeout(f, 100);
                } else {
                    window.scroll(0, 0);
                    document.title += "scroll-done";
                }
            }

            setTimeout(f, 1000);
        })();
    """)
    #wait
    if testmode:
        print 'scroll down ...'
    for i in xrange(30):
        if 'scroll-done' in driver.title:
            break
        sleep(1)


    driver.save_screenshot(filename)
    driver.close()
    if testmode:
        print 'finished:{} as {} ...'.format(address, filename)

if __name__ == '__main__':

    take_scrnshot('http://www.bilibili.com','e.png',True)