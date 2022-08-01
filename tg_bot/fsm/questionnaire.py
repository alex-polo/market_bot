from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import Message
from loguru import logger

# timeframes = ['1m', '5m', '15m', '30m', '1h', '4h', '1d']
timeframes = {'1m': 'не задано',
              '5m': 'не задано',
              '15m': 'не задано',
              '30m': 'не задано',
              '1h': 'не задано',
              '4h': 'не задано',
              '1d': 'не задано'}
markets = ['Binance', 'OKX', 'Binance&OKX']
signals = ['PUMP && DUMP', 'Divergense']
percents = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]


class FSMSubscribesAdmin(StatesGroup):
    waiting_market = State()
    waiting_signal = State()
    waiting_timeframes = State()
    waiting_percent = State()


async def subscription(message: Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for market in markets:
        keyboard.add(market)
    await message.answer("Выберите рынок:", reply_markup=keyboard)
    await FSMSubscribesAdmin.waiting_market.set()


async def detect_market(message: Message, state: FSMContext):
    if message.text not in markets:
        await message.answer('Пожалуйста, выберите значение ниже:')
        return

    # await state.update_data(chosen_market=message.text)
    async with state.proxy() as data:
        data['market'] = message.text

    # Отдаем рользователю меню для выбора сигнала
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for signal in signals:
        keyboard.add(signal)

    await message.answer("Выберете сигнал:", reply_markup=keyboard)
    await FSMSubscribesAdmin.waiting_signal.set()

def _keyboard_select_timeframes():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = [f'{tm_key} | {tm_value}' for tm_key, tm_value in timeframes.items()]
    buttons.append('Продолжить')
    keyboard.add(*buttons)
    return keyboard
async def detect_signal(message: Message, state: FSMContext):
    if message.text not in signals:
        await message.answer('Пожалуйста, выберите значение ниже:')
        return

    async with state.proxy() as data:
        data['signal'] = message.text

    # Отдаем пользователю меню для выбора таймфрема
    async with state.proxy() as data:
        data['timeframes'] = list()
        data['updating_timeframes'] = list()
    await message.answer("Задайте таймфрейм и процент для отслеживания:", reply_markup=_keyboard_select_timeframes())
    await FSMSubscribesAdmin.waiting_timeframes.set()


async def detect_timeframes(message: Message, state: FSMContext):
    logger.info(message.text)
    if message.text != 'Продолжить':
        timeframe = message.text.split(' | ')[0]
        async with state.proxy() as data:
            if len(data['updating_timeframes']):
                data['update_timeframe'] = timeframe
                if timeframe not in data['timeframes']:
                    data['timeframes'].append({
                        timeframe: None
                    })

        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        buttons = [f'{str(value)} %' for value in percents]
        buttons.append('Удалить значение')
        keyboard.add(*buttons)
        await message.answer("Выберите процент:", reply_markup=keyboard)
        await FSMSubscribesAdmin.waiting_percent.set()
        return
    else:
        async with state.proxy() as data:
            for key, value in data.items():
                print(key, value)
        await state.finish()
        await message.answer('Cancel', reply_markup=types.ReplyKeyboardRemove())


async def detect_percent(message: Message, state: FSMContext):
    logger.info(message.text)
    async with state.proxy() as data:
        # data['change_percent'] = message.text
        data['timeframes'][-1].set()
    await message.answer("Задайте таймфрейм и процент для отслеживания:", reply_markup=_keyboard_select_timeframes())
    await FSMSubscribesAdmin.waiting_timeframes.set()


def register_fsm_admin_questionnaire(dp: Dispatcher):
    dp.register_message_handler(subscription, commands=["subscription"], state='*', is_admin=True)
    dp.register_message_handler(detect_market, state=FSMSubscribesAdmin.waiting_market)
    dp.register_message_handler(detect_signal, state=FSMSubscribesAdmin.waiting_signal)
    dp.register_message_handler(detect_timeframes, state=FSMSubscribesAdmin.waiting_timeframes)
    dp.register_message_handler(detect_percent, state=FSMSubscribesAdmin.waiting_percent)
