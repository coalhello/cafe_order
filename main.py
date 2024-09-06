import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic

cafe_ui = uic.loadUiType("cafe.ui")[0]
order_ui = uic.loadUiType("order.ui")[0]

menu = [["코코아", 1000, 1500], ["카페라떼", 2000, 2500],
        ["밀크쉐이크", 3000, 3500], ["리스트레토", 4000, 4500]]

recent_order = "코코아"
recent_sort = "ice"
recent_shot = "샷 없음"
recent_num = "0"

final_order = []

class order(QMainWindow, order_ui):
    def __init__(self, parent=None):
        super().__init__()
        self.setupUi(self)

        self.parent = parent

        self.buttonGroup = QButtonGroup(self)
        self.buttonGroup.addButton(self.ice_checkbox, 1)
        self.buttonGroup.addButton(self.hot_checkbox, 2)
        self.menu_label.setText("메뉴 : " + f'{recent_order}')

        global recent_shot
        recent_shot = "샷 없음"

    def ice_clicked(self):
        global recent_sort
        recent_sort = "ice"

    def hot_clicked(self):
        global recent_sort
        recent_sort = "hot"

    def shot_changed(self, data):
        global recent_shot
        if data == 0:
            recent_shot = "샷 없음"
            self.shotcost_label.setText(recent_shot)
        elif data == 1:
            recent_shot = "샷 추가(+500원)"
            self.shotcost_label.setText(recent_shot)
        else:
            recent_shot = "투샷 추가(+1000원)"
            self.shotcost_label.setText(recent_shot)

    def check_clicked(self):
        global recent_num
        recent_num = self.num_line.text()

        recent_cost = 0
        for temp in menu:
            if temp[0] == recent_order:
                if recent_sort == "ice": recent_cost = temp[1]
                elif recent_sort == "hot": recent_cost = temp[2]
                if recent_shot == "샷 추가(+500원)": recent_cost += 500
                elif recent_shot == "투샷 추가(+1000원)": recent_cost += 1000
        recent_cost = recent_cost * int(recent_num)

        list = [recent_order, recent_sort, recent_shot, recent_num, recent_cost]
        final_order.append(list)

        temp = recent_order + ' / ' + recent_sort + ' / ' + recent_shot + ' / ' + recent_num + '잔 / ' + str(recent_cost) + '원'

        self.parent.order_listbox.addItem(temp)
        self.close()

    def cancel_clicked(self):
        self.close()

class cafe(QMainWindow, cafe_ui):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

    def cocoa_clicked(self):
        global recent_order
        recent_order = menu[0][0]
        self.order_window = order(self)
        self.order_window.show()

    def latte_clicked(self):
        global recent_order
        recent_order = menu[1][0]
        self.order_window = order(self)
        self.order_window.show()

    def milkshake_clicked(self):
        global recent_order
        recent_order = menu[2][0]
        self.order_window = order(self)
        self.order_window.show()

    def ristretto_clicked(self):
        global recent_order
        recent_order = menu[3][0]
        self.order_window = order(self)
        self.order_window.show()

    def delete_clicked(self):
        selected_row = self.order_listbox.currentRow()

        if selected_row >= 0:
            self.order_listbox.takeItem(selected_row)
            del final_order[selected_row]
        else:
            QMessageBox.warning(self, "오류", "항목을 고르고 결정해주세요!")

    def order_clicked(self):
        total = 0
        for temp in final_order:
            total += temp[4]
        reply = QMessageBox.question(self, '주문 안내', f'정말 주문하시겠습니까?({total}원)',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            if total == 0:
                QMessageBox.warning(self, "오류", "주문할 메뉴가 없어요!")
            else:
                QMessageBox.information(self, "주문 완료", "여기 음료입니다")
                self.close()
        else:
            return None

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = cafe()
    window.show()
    app.exec_()
