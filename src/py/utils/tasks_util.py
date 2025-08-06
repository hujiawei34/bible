"""
异步任务工具类

"""
import concurrent.futures
from typing import Callable, List, Any, Tuple
from src.py.utils.log_util import default_logger as logger

def run_with_thread_pool(func: Callable, args_list: List[Tuple], max_workers: int = 10) -> List[Any]:
    """
    使用线程池执行任务
    
    Args:
        func: 要执行的函数
        args_list: 参数列表，每个元素是一个元组，包含函数的参数
        max_workers: 最大线程数，默认为10
        
    Returns:
        结果列表
    """
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = []
        for args in args_list:
            if isinstance(args, tuple):
                future = executor.submit(func, *args)
            else:
                future = executor.submit(func, args)
            futures.append(future)
        
        for future in concurrent.futures.as_completed(futures):
            try:
                result = future.result()
                results.append(result)
            except Exception as e:
                logger.error(f"执行任务时出错: {str(e)}")
                results.append(None)
    
    return results